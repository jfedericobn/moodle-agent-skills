# Compatibility

Moodle 5.3 LTS is the primary development target. Moodle 4.5 LTS is the first compatibility target. Moodle 5.1 and 5.2 can be identified by the detector when their metadata is present. Treat them as unverified for task behavior. Use an explicit project version when provided.

The 5.1 public directory split affects web-root paths, even though framework files such as the component map can remain outside that directory. Plugin metadata describes a plugin and a minimum core requirement. It cannot establish a live site's release. [Moodle releases](https://moodledev.io/general/releases) and the [layout change](https://moodledev.io/docs/5.1/devupdate) describe these baselines.

Tests cover the installer and the detector. Actual agent activation and live Moodle scenario execution require their respective environments. Until those runs have been recorded, support means documented package paths and validated skill files. Follow the target branch's APIs and runtime requirements, and prefer its project instructions for command selection.
