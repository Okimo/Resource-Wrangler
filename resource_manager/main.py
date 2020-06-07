import argparse
import os

import toml
from resource_manager import runners

ENV_VAR_PIPELINES_CONFIG = "RESOURCE_MANAGER_PIPELINES_PATH"
ENV_VAR_RESOURCES_CONFIG = "RESOURCE_MANAGER_RESOURCES_PATH"


def main():
    parser = argparse.ArgumentParser(description='Minecraft resource manager')
    parser.add_argument('-p', '--pipelines', help='Pipelines config', required=False)
    parser.add_argument('-r', '--resources', help='Resources config', required=False)
    parser.add_argument('pipeline', help='Choose a sequence of tasks')
    args = parser.parse_args()

    if args.pipelines is None:
        args.config = os.environ.get(ENV_VAR_PIPELINES_CONFIG)

    if args.pipelines is None:
        print("Using default package pipelines.")
        args.pipelines = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs", "pipelines.toml")

    if args.resources is None:
        args.resources = os.environ.get(ENV_VAR_RESOURCES_CONFIG)

    if args.resources is None:
        print("Using default package resources.")
        args.resources = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs", "resources.toml")

    #
    # LOAD CONFIGS
    with open(args.resources, "r") as resources_file:
        resources = toml.load(resources_file)
    with open(args.pipelines, "r") as pipelines_file:
        pipelines = toml.load(pipelines_file)

    #
    # EXECUTE PIPELINE
    runners.run_pipeline({'pipeline': args.pipeline}, resources, pipelines)


if __name__ == "__main__":
    main()