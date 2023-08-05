import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pkgs = setuptools.find_packages()
print('found these packages:', pkgs)

pkg_name='ml_ephys'

setuptools.setup(
    name=pkg_name,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
#    version="0.2.6",
    author="Jeremy Magland",
    author_email="",
    description="ephys tools for MountainLab",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magland/ml_ephys",
    packages=pkgs,
    package_data={
        # Include all processor files
        '': ['*.mp']
    },
    install_requires=
    [
        'numpy',
        'mountainlab_pytools',
        'deepdish',
        'scipy',
        'numpydoc',
        'h5py'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    conda={
        "build_number":0,
        "build_script":[
            "python -m pip install --no-deps --ignore-installed .",
            "CMD=\"ln -sf $SP_DIR/"+pkg_name+" `CONDA_PREFIX=$PREFIX ml-config package_directory`/"+pkg_name+"\"",
            "echo $CMD",
            "$CMD"
        ],
        "test_commands":[
            "ml-list-processors",
            "ml-spec ephys.bandpass_filter"
        ],
        "test_imports":[
            "ml_ephys",
            "ml_ephys.basic",
            "ml_ephys.preprocessing",
            "ml_ephys.synthesis",
            "ml_ephys.validation"
        ],
        "requirements":[
            "python",
            "pip",
            "mountainlab",
            "mountainlab_pytools",
            "deepdish",
            "scipy",
            "numpy",
            "numpydoc",
            "h5py"
        ]
    }
)
