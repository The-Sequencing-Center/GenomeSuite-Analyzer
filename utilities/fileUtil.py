# Author:  Richard Casey
# Date:    07-10-2024 (DD-MM-YYYY)
# Purpose: Utility function to delete all files in subdirectories.  
#          Use to set initial conditions before starting application.
#          Use with caution.

# Standard library imports
import os
import shutil

def clear_files():
    """
    Delete all files in subdirectories. 
    Use to set initial conditions before starting application.
    Use with caution.
    """

    # delete existing pod5 files
    pod5_files_dir = os.environ.get('POD5_FILES_DIR')

    if pod5_files_dir:
        for filename in os.listdir(pod5_files_dir):
            file_path = os.path.join(pod5_files_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # delete existing fast5 files
    fast5_files_dir = os.environ.get('FAST5_FILES_DIR')

    if fast5_files_dir:
        for filename in os.listdir(fast5_files_dir):
            file_path = os.path.join(fast5_files_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # delete existing bam files
    bam_files_dir = os.environ.get('BAM_FILES_DIR')

    if bam_files_dir:
        for filename in os.listdir(bam_files_dir):
            file_path = os.path.join(bam_files_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # delete existing analyzer output files
    analyzer_files_dir = os.environ.get('ANALYZER_FILES_DIR')

    if analyzer_files_dir:
        for filename in os.listdir(analyzer_files_dir):
            file_path = os.path.join(analyzer_files_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # delete existing log files
    log_files_dir = os.environ.get('LOG_FILES_DIR')

    if log_files_dir:
        for filename in os.listdir(log_files_dir):
            file_path = os.path.join(log_files_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

# main entry point
if __name__ == "__main__":

    print("Clear all files...")

    # Set environment variables
    # os.environ['POD5_FILES_DIR']     = '/home/seqcenter/analyzer/data/INPUTS/POD5_FILES'
    # os.environ['FAST5_FILES_DIR']    = '/home/seqcenter/analyzer/data/INPUTS/FAST5_FILES'
    os.environ['BAM_FILES_DIR']      = '/home/seqcenter/analyzer/data/INPUTS/BAM_FILES'
    os.environ['ANALYZER_FILES_DIR'] = '/home/seqcenter/analyzer/data/OUTPUTS/analyzer_output'
    os.environ['LOG_FILES_DIR']      = '/home/seqcenter/analyzer/logs'

    clear_files()

    print("Done.") 
