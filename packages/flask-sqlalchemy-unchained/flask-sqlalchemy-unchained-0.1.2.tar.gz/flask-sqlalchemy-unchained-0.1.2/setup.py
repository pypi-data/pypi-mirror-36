from setuptools import setup


setup(
    name='flask-sqlalchemy-unchained',
    version='0.1.2',
    description='Integrates SQLAlchemy Unchained with Flask',
    author='Brian Cappello',
    license='MIT',

    py_modules=['flask_sqlalchemy_unchained'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'flask-sqlalchemy>=2.3.1',
        'sqlalchemy-unchained>=0.2.2',
    ],
    extras_require={
        'dev': [
            'coverage',
            'factory_boy',
            'm2r',
            'mock',
            'pytest',
            'pytest-flask',
            'tox',
        ],
        'docs': [
            'sphinx',
            'sphinx-autobuild',
            'sphinx-click',
            'sphinx-rtd-theme',
        ],
    },

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
