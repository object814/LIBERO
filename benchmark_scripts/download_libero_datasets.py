import init_path
import argparse
import os
import time
from urllib.error import URLError
from socket import timeout

import libero.libero.utils.download_utils as download_utils
from libero.libero import get_libero_path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--download-dir",
        type=str,
        default=get_libero_path("datasets"),
    )
    parser.add_argument(
        "--datasets",
        type=str,
        choices=["all", "libero_goal", "libero_spatial", "libero_object", "libero_100"],
        default="all",
    )
    return parser.parse_args()


def download_with_retries(download_func, max_retries=5, wait_time=10, **kwargs):
    """Retry downloading in case of connection errors."""
    retries = 0
    while retries < max_retries:
        try:
            download_func(**kwargs)
            print("Download successful.")
            return  # Exit if successful
        except (URLError, ConnectionResetError, timeout) as e:
            retries += 1
            print(f"Error: {e}")
            print(f"Retrying {retries}/{max_retries} after {wait_time} seconds...")
            time.sleep(wait_time)
    print(f"Failed to download after {max_retries} retries.")


def main():
    args = parse_args()

    # Ask users to specify the download directory of datasets
    os.makedirs(args.download_dir, exist_ok=True)
    print(f"Datasets downloaded to {args.download_dir}")
    print(f"Downloading {args.datasets} datasets")
    print(f"Runtime: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    # Download with retries
    download_with_retries(
        download_func=download_utils.libero_dataset_download,
        max_retries=5,
        wait_time=10,
        download_dir=args.download_dir,
        datasets=args.datasets,
    )

    # Check if datasets exist after download
    try:
        download_utils.check_libero_dataset(download_dir=args.download_dir)
    except Exception as e:
        print(f"Error checking datasets: {e}")


if __name__ == "__main__":
    main()
