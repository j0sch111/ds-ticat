#!/bin/bash
# This is all one-time setup and will be skipped on updates


destination_root=$1
current_directory=$(pwd)

if [[ $PWD == /tmp* ]]; then
    echo "Skipping tasks, this is an update!"
    exit 0
fi
if [[ $PWD == /private/var* ]]; then
    echo "Skipping tasks, this is an update!"
    exit 0
fi

echo "Running the post-copier setup script..."
if [ -d .git/ ]; then
  echo "This project is already initialized. Exiting"
  exit 0
fi
echo "Creating your git repository..."
git init $destination_root
git -C $destination_root checkout -b main
git -C $destination_root add .
git -C $destination_root commit -m "Initial Commit from DS Python Template 🎉"
git -C $destination_root checkout -b development

echo "Creating your python envs..."
pixi install -e dev --manifest-path $destination_root/pyproject.toml

echo "Installing Pre-commit hooks"
cd $destination_root
pre-commit install
cd $current_directory

echo "Creating your python envs..."
pixi install --manifest-path $destination_root/pyproject.toml

echo "Installing Pre-commit hooks"
cd $destination_root
pre-commit install
cd $current_directory

cat << EOF



👷 <( Project creation complete! )

Command + Click here to open your project:
> $destination_root

and here to read the Quick start:
> $destination_root/README.md


EOF
