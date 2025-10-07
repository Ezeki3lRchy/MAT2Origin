# mat2csv.py
import sys, os
import numpy as np
import pandas as pd

def save_array(arr, outbase, varname):
    def write2d(A, suffix=""):
        pd.DataFrame(A).to_csv(f"{outbase}_{varname}{suffix}.csv", index=False)

    if np.iscomplexobj(arr):        # split complex into real/imag CSVs
        A = np.asarray(arr)
        if A.ndim <= 2:
            write2d(A.real, "_real")
            write2d(A.imag, "_imag")
        elif A.ndim == 3:
            for k in range(A.shape[2]):
                write2d(A[:,:,k].real, f"_real_slice{k:03d}")
                write2d(A[:,:,k].imag, f"_imag_slice{k:03d}")
        else:
            A2 = A.reshape(A.shape[0], -1)
            write2d(A2.real, "_real_flat")
            write2d(A2.imag, "_imag_flat")
        return

    A = np.asarray(arr)
    if A.ndim <= 2:
        write2d(A)
    elif A.ndim == 3:
        for k in range(A.shape[2]):
            write2d(A[:,:,k], f"_slice{k:03d}")
    else:
        A2 = A.reshape(A.shape[0], -1)
        write2d(A2, "_flat")

def export_mat_v7(mat_path):
    from scipy.io import loadmat
    mdict = loadmat(mat_path, squeeze_me=True, struct_as_record=False)
    base = os.path.splitext(os.path.basename(mat_path))[0]
    skipped = []
    for k, v in mdict.items():
        if k.startswith("__"):
            continue
        try:
            # numeric/logical/char arrays will work; structs/cells won’t
            save_array(v, base, k)
        except Exception as e:
            skipped.append((k, str(e)))
    return skipped

def export_mat_v73(mat_path):
    import h5py
    base = os.path.splitext(os.path.basename(mat_path))[0]
    skipped = []
    with h5py.File(mat_path, "r") as f:
        def walk(g, prefix=""):
            for name, obj in g.items():
                path = f"{prefix}{name}"
                if isinstance(obj, h5py.Dataset):
                    try:
                        data = obj[()]
                        if np.issubdtype(np.asarray(data).dtype, np.number) or np.iscomplexobj(data):
                            save_array(data, base, path.replace('/', '_'))
                        else:
                            skipped.append((path, "non-numeric dataset"))
                    except Exception as e:
                        skipped.append((path, str(e)))
                elif isinstance(obj, h5py.Group):
                    walk(obj, prefix=path + "/")
        walk(f, "")
    return skipped

def main():
    if len(sys.argv) != 2:
        print("Usage: python mat2csv.py your_file.mat")
        sys.exit(1)
    mat_path = sys.argv[1]
    # Try SciPy first (v7). If NotImplementedError, try v7.3 (HDF5) with h5py.
    try:
        skipped = export_mat_v7(mat_path)
    except NotImplementedError:
        skipped = export_mat_v73(mat_path)
    except Exception as e:
        # if SciPy fails for other reasons, attempt v7.3 anyway
        try:
            skipped = export_mat_v73(mat_path)
        except Exception as e2:
            print("Failed to read MAT file with both methods:\n", e, "\n", e2)
            sys.exit(2)

    if skipped:
        print("Some variables/datasets were skipped:")
        for k, msg in skipped:
            print(f"  - {k}: {msg}")

if __name__ == "__main__":
    main()
