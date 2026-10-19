# Environment checks and recovery

## Normal Google Colab use

Open the current notebook in a fresh CPU runtime and choose **Runtime → Run all**. Part 0.1 imports the preinstalled scientific packages, prints both loaded and installed versions, and checks the interfaces used by the tutorial. It runs no pip command and does not require versions to equal the local pins. The five model steps are unchanged.

Checks include importing scikit-learn's ensemble/model-selection/metric APIs, checking PyTorch's `weights_only` argument, exchanging a NumPy array with PyTorch, creating a pandas table, calculating a known AUC and rendering a tiny matplotlib figure. These are operational checks, not a guarantee for every possible dependency combination. The subsequent full tutorial provides the actual scientific execution test. Recorded package versions accompany each generated result.

## Recover from the reported NumPy import error

`ImportError: cannot import name '_slice' from numpy._core.umath` is consistent with an inconsistent installation or loaded state. The exact failed runtime was not available for inspection, so no unique cause is asserted. The previous notebook could replace already-loaded compiled packages to enforce local pins; that behavior has been removed.

1. Stop running cells after an import failure.
2. If packages were installed during the session, restart the Python runtime, then Run all with the updated notebook.
3. If imports still fail, preserve any needed files from the temporary runtime, select **Runtime → Disconnect and delete runtime**, reconnect, and Run all. This restores Colab's default runtime; it discards files stored only in that temporary runtime. The notebook will retrieve its dataset/checkpoint again.
4. Do not use `importlib.reload`, reinstall NumPy repeatedly, or continue executing with partially imported scientific modules.

## Controlled installation when genuinely necessary

If a package is actually absent, inspect the error and install only that identified package in a separate manual cell (`%pip install PACKAGE_NAME`, replacing the placeholder with the named missing package). Do not use the pinned local requirements to replace a healthy Colab stack. A version difference alone is not an incompatibility.

If a required API is genuinely unavailable (for example PyTorch lacks `weights_only` support), select a compatible package version and dependencies based on that API requirement. Prefer restoring a fresh Colab default runtime before changing compiled dependencies. The setup cell deliberately does not guess a universal repair version.

**After any manual installation, STOP and restart the Python runtime before Run all.** Installation is not part of automatic Run all, and no branch silently installs and continues. If restarted imports still fail, restore the default runtime rather than retrying package replacements in place.

## Reproducible local execution

The original requirements.txt is unchanged. Install it before starting a notebook kernel:

```sh
python -m venv .venv
# Activate .venv using your platform's standard activation command.
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyter lab
```

Select that environment's kernel. If an existing kernel was running during installation, restart it. A separate compatible dependency stack can execute the same model but may produce small numerical differences; do not alter fitting to force equality. Reference results remain in results/ and measured comparisons appear in VERIFICATION_REPORT.md.

## Sources

[NumPy import troubleshooting](https://numpy.org/doc/stable/user/troubleshooting-importerror.html) describes installation and downstream binary-compatibility failures. [Google Colab FAQ](https://research.google.com/colaboratory/faq.html) documents restoring a runtime with Disconnect and delete runtime. Runtime restoration and a Python-kernel restart are distinct operations.
