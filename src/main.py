#!/usr/bin/env python3
"""
Input: POTA activation data
Output: ADIF file for upload to https://pota.app/
"""
import os
import argparse
from gnupass import Secret
import config
import adif
import pota
import logging


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fin", required=True)
    parser.add_argument("--fout", required=True)
    parser.add_argument("--fdbg", required=True)
    parser.add_argument("--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info(f"APP_VERSION: {config.APP_VERSION}")
    logging.info(f"BUILD_TIME: {config.BUILD_TIME}")

    palog = pota.ActivationLog()
    palog.read_yaml(args.fin)
    palog.augment_with_qrz()
    palog.write_yaml(args.fdbg)
    palog.write_adif(args.fout)
