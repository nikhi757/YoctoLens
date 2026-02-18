YoctoLens

YoctoLens is an intelligent build failure analyzer for Yocto Project builds.

It parses BitBake logs, identifies root causes of failures, categorizes errors, and provides structured debugging guidance — with future support for AI-assisted fixes and automated pull request generation.

Why YoctoLens?

Yocto build failures are often:

Verbose and difficult to trace

Spread across multiple layers

Indirect in root cause

Time-consuming to debug

Difficult for junior engineers

YoctoLens aims to reduce debugging time by providing:

Structured error extraction

Deterministic failure classification

Context-aware suggestions

Future automated fix generation

Current Scope (v0.1 – In Progress)

Extract failing task from BitBake logs

Identify recipe and task context

Classify common Yocto error types:

Nothing PROVIDES

file-rdeps issues

do_package_qa failure

Patch failures

Fetch failures

Structured CLI output

Optional JSON output mode

Planned Roadmap
Phase 1 – Core Engine

Log parser

Error taxonomy

Structured classification

Phase 2 – Intelligent Suggestions

AI-assisted root cause reasoning

Fix templates

Confidence scoring

Phase 3 – Fix Automation

bbappend generator

Safe workspace modifications

Git branch + commit automation

Optional pull request generation

Installation (Development Mode)

Clone the repository:

git clone https://github.com/nikhi757/YoctoLens.git

cd YoctoLens

Run:

python cli.py analyze build.log

Packaging and pip installation support will be added in future releases.

Usage (Planned CLI Interface)

Analyze a build log:

yoctolens analyze build.log

Get structured JSON output:

yoctolens analyze build.log --json

Generate suggested fix:

yoctolens suggest build.log

Dry-run patch preview:

yoctolens fix build.log --dry-run

Design Principles

Deterministic first, AI second

Human approval before applying changes

Minimal hallucination risk

Focused on Yocto Project builds

Built by embedded engineers for embedded engineers

License

Licensed under the Apache License 2.0.
See the LICENSE file for details.

Contributing

Contributions are welcome.

Before submitting a pull request:

Ensure code is tested

Follow project structure

Add sample log cases if introducing new classifiers

To report an issue:

Include Yocto version

Include failing task

Attach relevant log snippet

Project Status

Early development.

Open to feedback from the Yocto and embedded Linux community.

Vision

YoctoLens aims to become:

“The intelligent debugging assistant for embedded build systems.”

Starting with Yocto.
Expanding to other build systems in the future.
