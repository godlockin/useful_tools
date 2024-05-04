from concurrent.futures import ThreadPoolExecutor
import subprocess
import argparse
import os

def git_pull(folder):
    if os.path.exists(os.path.join(folder, '.git')):
        print(f"Performing 'git pull' in {folder}")
        process = subprocess.Popen(['git', '-C', folder, 'pull', '--ff-only'], stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            print(f"Error pulling in {folder}: {err.decode()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform git pull recursively.')
    parser.add_argument('base_url', type=str, help='The base directory to start pulling.')
    parser.add_argument('--skip_folders', type=str, default='', help='Folders to skip, separated by comma.')
    args = parser.parse_args()

    skip_folders = args.skip_folders.split(',') if args.skip_folders else []
    skip_folders.append('.git')
    skip_folders.append('.github')

    print(f"try to update {args.base_url} as root")

    # 获取所有的目录
    folders = [os.path.join(root, dir_name) for root, dirs, _ in os.walk(args.base_url) for dir_name in dirs if dir_name not in skip_folders and '.git' not in dirs]
    # 跳过 .git 文件夹
    folders = [item for item in folders if '.git' not in item]
    print("\n".join(sorted(folders)))

    # 使用线程池来并行执行git pull
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(git_pull, folders)