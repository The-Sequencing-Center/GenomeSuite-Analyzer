# Name:    GenomeSuite Analyzer
# Author:  Richard Casey
# Date:    09-02-2024 (DD-MM-YYYY)
# Purpose: Human genome structural variant caller.
# Version: v.1.2.0
# Notes:   In production mode, this application requires Nvidia GPU's (H100, A100, V100).

# Standard library imports
import argparse
import os
import subprocess
import sys

# Third-party imports
import boto3
from   botocore.exceptions import ClientError
from   botocore.exceptions import NoCredentialsError
from   botocore.exceptions import PartialCredentialsError

# Local application/library specific imports
from utilities.fileUtil   import clear_files
from utilities.loggerUtil import logger

def run_command(command: str) -> None:
    """Run a shell command and print the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"{result.stdout}")
        logger.info(f"{result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"ERROR: run_command failed with error: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        sys.exit(1)

def set_environment_variables(sample_name: str) -> None:
    """Set environment variables."""
    try:
        # check which server is hosting the code 
        home_dir = os.path.expanduser("~")                             # get home directory
        if home_dir   == '/home/seqcenter':
            os.environ['BASE_DIR'] = '/home/seqcenter/analyzer'        # for development ubuntu
        elif home_dir == '/home/ubuntu':
            os.environ['BASE_DIR'] = '/home/ubuntu/analyzer'           # for production ubuntu on AWS
        else:
            logger.error("ERROR: unknown home directory setting")
            sys.exit(1)
    except ValueError as e:
        logger.error(f"Error: an unexpected error occured{e}")
        sys.exit(1)

    # MAIN DIRS
    os.environ['INPUT_DIR']          = f"{os.environ['BASE_DIR']}/data/INPUTS"
    os.environ['OUTPUT_DIR']         = f"{os.environ['BASE_DIR']}/data/OUTPUTS"

    # POD5
    os.environ['POD5_FILES_DIR']     = f"{os.environ['INPUT_DIR']}/POD5_FILES"

    # FAST5
    os.environ['FAST5_FILES_DIR']    = f"{os.environ['INPUT_DIR']}/FAST5_FILES"

    # # BAM
    os.environ['BAM_FILES_DIR']      = f"{os.environ['INPUT_DIR']}/BAM_FILES"
    os.environ['BAM_FILE']           = f"{os.environ['INPUT_DIR']}/BAM_FILES/{sample_name}.bam"
    os.environ['BAM_SORTED_FILE']    = f"{os.environ['INPUT_DIR']}/BAM_FILES/{sample_name}.sorted.bam"

    # REFERENCE 
    os.environ['REF_FILES_DIR']      = f"{os.environ['INPUT_DIR']}/REF_FILES"
    os.environ['REF_FILE']           = f"{os.environ['INPUT_DIR']}/REF_FILES/GCA_009914755.4_T2T-CHM13v2.0_genomic.fna.gz"

    # # MODELS
    os.environ['DORADO_MODELS']      = f"{os.environ['BASE_DIR']}/dorado_models"

    # ANALYZER
    os.environ['ANALYZER_FILES_DIR'] = f"{os.environ['OUTPUT_DIR']}/analyzer_output"
    os.environ['ANALYZER_VCF_FILE']  = f"{os.environ['ANALYZER_FILES_DIR']}/{sample_name}.vcf.gz"

    # THREADS
    os.environ['THREADS']            = '14'

def check_s3_bucket_exists(bucket_name: str) -> bool:
    """Check if the specified S3 bucket exists."""
    s3 = boto3.client('s3')
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise
    except NoCredentialsError:
        logger.error("ERROR: AWS credentials not found.")
        sys.exit(1)
    except PartialCredentialsError:
        logger.error("ERROR: Incomplete AWS credentials.")
        sys.exit(1)

def dorado_models():
    """List of available dorado models"""
    models = [
        "dna_r10.4.1_e8.2_260bps_fast@v3.5.2",
        "dna_r10.4.1_e8.2_260bps_fast@v3.5.2_5mCG@v2",
        "dna_r10.4.1_e8.2_260bps_fast@v4.0.0",
        "dna_r10.4.1_e8.2_260bps_fast@v4.0.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_260bps_fast@v4.1.0",
        "dna_r10.4.1_e8.2_260bps_fast@v4.1.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_260bps_hac@v3.5.2",
        "dna_r10.4.1_e8.2_260bps_hac@v3.5.2_5mCG@v2",
        "dna_r10.4.1_e8.2_260bps_hac@v4.0.0",
        "dna_r10.4.1_e8.2_260bps_hac@v4.0.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_260bps_hac@v4.1.0",
        "dna_r10.4.1_e8.2_260bps_hac@v4.1.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_260bps_sup@v3.5.2",
        "dna_r10.4.1_e8.2_260bps_sup@v3.5.2_5mCG@v2",
        "dna_r10.4.1_e8.2_260bps_sup@v4.0.0",
        "dna_r10.4.1_e8.2_260bps_sup@v4.0.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_260bps_sup@v4.1.0",
        "dna_r10.4.1_e8.2_260bps_sup@v4.1.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_fast@v3.5.2",
        "dna_r10.4.1_e8.2_400bps_fast@v3.5.2_5mCG@v2",
        "dna_r10.4.1_e8.2_400bps_fast@v4.0.0",
        "dna_r10.4.1_e8.2_400bps_fast@v4.0.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_fast@v4.1.0",
        "dna_r10.4.1_e8.2_400bps_fast@v4.1.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_fast@v4.2.0",
        "dna_r10.4.1_e8.2_400bps_fast@v4.2.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_fast@v4.3.0",
        "dna_r10.4.1_e8.2_400bps_fast@v5.0.0",
        "dna_r10.4.1_e8.2_400bps_hac@v3.5.2",
        "dna_r10.4.1_e8.2_400bps_hac@v3.5.2_5mCG@v2",
        "dna_r10.4.1_e8.2_400bps_hac@v4.0.0",
        "dna_r10.4.1_e8.2_400bps_hac@v4.0.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_hac@v4.1.0",
        "dna_r10.4.1_e8.2_400bps_hac@v4.1.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_hac@v4.2.0",
        "dna_r10.4.1_e8.2_400bps_hac@v4.2.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_hac@v4.3.0",
        "dna_r10.4.1_e8.2_400bps_hac@v4.3.0_5mC_5hmC@v1",
        "dna_r10.4.1_e8.2_400bps_hac@v4.3.0_5mCG_5hmCG@v1",
        "dna_r10.4.1_e8.2_400bps_hac@v4.3.0_6mA@v1",
        "dna_r10.4.1_e8.2_400bps_hac@v4.3.0_6mA@v2",
        "dna_r10.4.1_e8.2_400bps_hac@v5.0.0",
        "dna_r10.4.1_e8.2_400bps_hac@v5.0.0_4mC_5mC@v1",
        "dna_r10.4.1_e8.2_400bps_hac@v5.0.0_5mC_5hmC@v1",
        "dna_r10.4.1_e8.2_400bps_hac@v5.0.0_5mCG_5hmCG@v1",
        "dna_r10.4.1_e8.2_400bps_hac@v5.0.0_6mA@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v3.5.2",
        "dna_r10.4.1_e8.2_400bps_sup@v3.5.2_5mCG@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v4.0.0",
        "dna_r10.4.1_e8.2_400bps_sup@v4.0.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v4.1.0",
        "dna_r10.4.1_e8.2_400bps_sup@v4.1.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0_5mC_5hmC@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0_5mCG_5hmCG@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0_5mCG_5hmCG@v3.1",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0_5mC@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0_6mA@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v4.2.0_6mA@v3",
        "dna_r10.4.1_e8.2_400bps_sup@v4.3.0",
        "dna_r10.4.1_e8.2_400bps_sup@v4.3.0_5mC_5hmC@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v4.3.0_5mCG_5hmCG@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v4.3.0_6mA@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v4.3.0_6mA@v2",
        "dna_r10.4.1_e8.2_400bps_sup@v5.0.0",
        "dna_r10.4.1_e8.2_400bps_sup@v5.0.0_4mC_5mC@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v5.0.0_5mC_5hmC@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v5.0.0_5mCG_5hmCG@v1",
        "dna_r10.4.1_e8.2_400bps_sup@v5.0.0_6mA@v1",
        "dna_r10.4.1_e8.2_4khz_stereo@v1.1",
        "dna_r10.4.1_e8.2_5khz_stereo@v1.1",
        "dna_r10.4.1_e8.2_5khz_stereo@v1.2",
        "dna_r10.4.1_e8.2_5khz_stereo@v1.3",
        "dna_r10.4.1_e8.2_apk_sup@v5.0.0",
        "dna_r9.4.1_e8_fast@v3.4",
        "dna_r9.4.1_e8_fast@v3.4_5mCG_5hmCG@v0",
        "dna_r9.4.1_e8_fast@v3.4_5mCG@v0.1",
        "dna_r9.4.1_e8_hac@v3.3",
        "dna_r9.4.1_e8_hac@v3.3_5mCG_5hmCG@v0",
        "dna_r9.4.1_e8_hac@v3.3_5mCG@v0.1",
        "dna_r9.4.1_e8_sup@v3.3",
        "dna_r9.4.1_e8_sup@v3.3_5mCG_5hmCG@v0",
        "dna_r9.4.1_e8_sup@v3.3_5mCG@v0.1",
        "dna_r9.4.1_e8_sup@v3.6",
        "rna002_70bps_fast@v3",
        "rna002_70bps_hac@v3",
        "rna004_130bps_fast@v3.0.1",
        "rna004_130bps_fast@v5.0.0",
        "rna004_130bps_hac@v3.0.1",
        "rna004_130bps_hac@v5.0.0",
        "rna004_130bps_hac@v5.0.0_m6A@v1",
        "rna004_130bps_hac@v5.0.0_pseU@v1",
        "rna004_130bps_sup@v3.0.1",
        "rna004_130bps_sup@v3.0.1_m6A_DRACH@v1",
        "rna004_130bps_sup@v5.0.0",
        "rna004_130bps_sup@v5.0.0_m6A@v1",
        "rna004_130bps_sup@v5.0.0_pseU@v1",
    ]
    return models

def print_dorado_models():
    """Print the list of available dorado models"""
    models = dorado_models()
    print("Available dorado model names:")
    for model in models:
        print(model)

def copy_pod5_sample_files_S3_to_EC2(bucket_name: str, sample_name: str) -> None:
    """Copy pod5 sample files from S3 to EC2.
    
     Parameters:
       --recursive : Copy files recursively.  This is a required parameter.
    """
    command = (
        f"aws s3 cp s3://{bucket_name}/ "
        f"{os.environ['POD5_FILES_DIR']} "
        "--recursive"
    )
    run_command(command)

def copy_fast5_sample_files_S3_to_EC2(bucket_name: str, sample_name: str) -> None:
    """Copy fast5 sample files from S3 to EC2.
    
     Parameters:
       --recursive : Copy files recursively.  This is a required parameter.
    """
    command = (
        f"aws s3 cp s3://{bucket_name}/ "
        f"{os.environ['FAST5_FILES_DIR']} "
        "--recursive"
    )
    run_command(command)

def convert_fast5_to_pod5(sample_name: str) -> None:
    """Convert FAST5 file to POD5 file. 
    In pod5 output directory, the default output filename is output.pod5. Rename this file using the "-s" parameter.

    Parameters:
       -o           : POD5 output directory.       
       -t           : Number of threads.
        sample_name : The name to use for renaming the output.pod5 file.
    """
    command = (
        "pod5 convert fast5 "
        f"   {os.environ['FAST5_FILES_DIR']} "
        f"-o {os.environ['POD5_FILES_DIR']} "
        f"-t {os.environ['THREADS']}"
    )
    run_command(command)

    # Rename output.pod5 file using the "-s" parameter
    try:
        original_file = os.path.join(os.environ['POD5_FILES_DIR'], "output.pod5")
        new_file      = os.path.join(os.environ['POD5_FILES_DIR'], f"{sample_name}.pod5")
        os.rename(original_file, new_file)
        logger.info(f"Renamed {original_file} to {new_file}")
    except Exception as e:
        logger.error(f"ERROR: Failed to rename output.pod5 to {sample_name}.pod5: {e}")
        sys.exit(1)

def get_gpu_architecture() -> str:
    """Determine if a Nvidia GPU with architecture Volta, Ampere or Hopper is available"""
    try:
        # Use nvidia-smi to get GPU info
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return None  # No Nvidia GPU detected
        gpu_name: str = result.stdout.strip()

        # Check for architectures of interest
        if any(arch in gpu_name for arch in ['Volta', 'Ampere', 'Hopper', 'H100']):
            return 'cuda'
        else:
            return 'cpu'
    except FileNotFoundError:
        return 'cpu'  # nvidia-smi not found, so assume no GPU is present
    
def convert_pod5_to_bam(modelname: str) -> None:
    """Convert POD5 file to BAM file using dorado basecaller.
    Note: In production mode, set "-x" to "cuda:all" so it uses Nvidia GPU's (H100, A100, V100).
    
    Parameters:
        -x : use cpu only or use gpu's. device string in format "cuda:0,...,N", "cuda:all", "metal", "cpu", etc.., [default: "cuda:all"]
    """

    # Determine whether to use CPU or GPU (GPU architecture must be Volta, Ampere or Hopper)
    gpu_arch = get_gpu_architecture()

    # Construct appropriate dorado command for CPU or GPU
    if gpu_arch == 'cuda':
        command = (
            "dorado basecaller "
            "-x cuda:all "
            f"--reference {os.environ['REF_FILE']} "
            f"            {os.environ['DORADO_MODELS']}/{modelname} "
            f"            {os.environ['POD5_FILES_DIR']} > "  # this parameter is either a single file name or a directory name (confusing)
            f"            {os.environ['BAM_FILE']}"
        )
    else:
        command = (
            "dorado basecaller "
            "-x cpu "
            f"--reference {os.environ['REF_FILE']} "
            f"            {os.environ['DORADO_MODELS']}/{modelname} "
            f"            {os.environ['POD5_FILES_DIR']} > "  # this parameter is either a single file name or a directory name (confusing)
            f"            {os.environ['BAM_FILE']}"
        )
    run_command(command)

def create_bam_index_file() -> None:
    """Create bam index file."""
    command = (
        "samtools index "
        f"-@ {os.environ['THREADS']} "
        f"   {os.environ['BAM_FILE']}"
    )
    run_command(command)

def sort_bam_file() -> None:
    """Sort bam file."""
    command = (
        "samtools sort "
        f"--threads {os.environ['THREADS']} "
        f"          {os.environ['BAM_FILE']} "
        f"-o        {os.environ['BAM_SORTED_FILE']}"
    )
    run_command(command)

def create_sorted_bam_index_file() -> None:
    """Create sorted bam index file."""
    command = (
        "samtools index "
        f"-@ {os.environ['THREADS']} "
        f"   {os.environ['BAM_SORTED_FILE']}"
    )
    run_command(command)

def run_analyzer() -> None:
    """
    Perform sturctural variant calling.

    Parameters:
        -i                : Input sorted BAM file.
        -v                : Output analyzer VCF file
        -t                : Number of threads.
    """

    command = (
        "sniffles "
        f"-i {os.environ['BAM_SORTED_FILE']} "
        f"-v {os.environ['ANALYZER_VCF_FILE']} "
        f"-t {os.environ['THREADS']}"
    )
    run_command(command)

def copy_vcf_file_to_s3(bucket_name: str, sample_name: str) -> None:
    """Copy the VCF file to the specified S3 bucket."""
    try:
        output_dir = os.environ['ANALYZER_FILES_DIR']
        vcf_file   = f"{output_dir}/{sample_name}.vcf.gz"
        command    = f"aws s3 cp {vcf_file} s3://{bucket_name}/"
        run_command(command)
    except Exception as e:
        logger.error(f"ERROR: Failed to copy VCF file to S3: {e}")
        sys.exit(1)
    
# main entry point
if __name__ == "__main__":

    try:
        # set S3 bucket name and sample name
        parser = argparse.ArgumentParser()
        parser.add_argument("-b", "--bucketname", help="Enter a bucket name for this run.")
        parser.add_argument("-s", "--samplename", help="Enter a sample name for this run.")
        parser.add_argument('-f', '--filetype',   help='Specify the type of input file: pod5 or fast5', choices=['pod5', 'fast5'])
        parser.add_argument('-m', '--modelname',  help="Specify the model name to use or omit to see available models. If not specified, default model will be used.", nargs='?')

        # Parse arguments
        args, unknown = parser.parse_known_args()

        # Check if only `-m` is provided
        if args.modelname is None and not args.bucketname and not args.samplename and not args.filetype:
            print_dorado_models()
            sys.exit(0)

        # If other required arguments are missing, show an error
        if not args.bucketname or not args.samplename or not args.filetype:
            logger.error("ERROR: the following arguments are required: -b/--bucketname, -s/--samplename, -f/--filetype")
            sys.exit(1)

        # Use default dorado model if one is not provided on command line
        modelname = args.modelname if args.modelname else "dna_r10.4.1_e8.2_4khz_stereo@v1.1"

        # Validate user supplied dorado model name against the list in dorado_models
        if modelname not in dorado_models():
            logger.error(f"ERROR: Model name '{modelname}' not found in the list of available models. Check your spelling for the model name.")
            print_dorado_models()
            sys.exit(1)

        # Start the run
        logger.info("Start Analyzer...")

        # set env vars
        try:
            logger.info("Set environment variables...")
            set_environment_variables(args.samplename)
        except Exception as e:
            logger.error(f"ERROR: Could not set environment variables {e}")
            sys.exit(1)

        # # delete all files in subdirectories to set initial state for application
        # try:
        #     logger.info("Clear files...")
        #     clear_files()
        # except Exception as e:
        #     logger.error(f"ERROR: Failed to clear files: {e}")

        # # Check if S3 bucket exists
        # try:
        #     if not check_s3_bucket_exists(args.bucketname):
        #         logger.error(f"ERROR: AWS S3 bucket '{args.bucketname}' does not exist.")
        #         sys.exit(1)
        # except NoCredentialsError:
        #     logger.error("ERROR: AWS credentials not found.")
        #     sys.exit(1)
        # except PartialCredentialsError:
        #     logger.error("ERROR: Incomplete AWS credentials.")
        #     sys.exit(1)
        # except Exception as e:
        #     logger.error(f"ERROR: An error occurred while checking the AWS S3 bucket: {e}")
        #     sys.exit(1)

        # # 1. copy pod5 or fast5 sample files from S3 seqcenter-samples bucket to EC2 POD5 or FAST5 directory
        # if args.filetype == "pod5":
        #     try:
        #         logger.info("Copy POD5 sample files from S3 to EC2...")
        #         copy_pod5_sample_files_S3_to_EC2(args.bucketname, args.samplename)
        #     except Exception as e:
        #         logger.error(f"ERROR: Failed to copy POD5 sample files from S3 to EC2: {e}")
        #         sys.exit(1)
        # elif args.filetype == "fast5":
        #     try:
        #         logger.info("Copy FAST5 sample files from S3 to EC2...")
        #         copy_fast5_sample_files_S3_to_EC2(args.bucketname, args.samplename)
        #     except Exception as e:
        #         logger.error(f"ERROR: Failed to copy FAST5 sample files from S3 to EC2: {e}")
        #         sys.exit(1)

        # # 2. convert fast5 file to pod5 file
        # if args.filetype == "fast5":
        #     try:
        #         logger.info("Convert fast5 to pod5...")
        #         convert_fast5_to_pod5(args.samplename)
        #     except Exception as e:
        #         logger.error(f"ERROR: Failed to convert fast5 to pod5: {e}")
        #         sys.exit(1)

        # 2. convert pod5 file to bam file
        try:
            logger.info("Convert pod5 to bam...")
            convert_pod5_to_bam(modelname)
        except Exception as e:
            logger.error(f"ERROR: Failed to convert pod5 to bam: {e}")
            sys.exit(1)

        # 3. sort bam file
        try:
            logger.info("Sort bam file...")
            sort_bam_file()
        except Exception as e:
            logger.error(f"ERROR: Failed to sort bam file: {e}")
            sys.exit(1)

        # 4. create sorted bam index file
        try:
            logger.info("Create sorted bam index file...")
            create_sorted_bam_index_file()
        except Exception as e:
            logger.error(f"ERROR: Failed to create sorted bam index file: {e}")
            sys.exit(1)

        # 5. perform structural variant calling
        try:
            logger.info("Perform structural variant calling...")
            run_analyzer()
        except Exception as e:
            logger.error(f"ERROR: Failed to perform structural variant calling: {e}")
            sys.exit(1)

        # # 6. copy VCF file to S3 bucket
        # try:
        #     logger.info("Copy VCF file to S3 bucket...")
        #     copy_vcf_file_to_s3(args.bucketname, args.samplename)
        # except Exception as e:
        #     logger.error(f"ERROR: Failed to copy VCF file to S3 bucket: {e}")
        #     sys.exit(1)

        # End the run
        logger.info("Finish Analyzer...")

    except Exception as e:
        logger.error(f"ERROR: an error occurred in main: {e}")
        sys.exit(1)
