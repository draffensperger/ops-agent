# Development

## Repo structure

<details>
  <summary>Config generation related</summary>

Description                                                                                                                                                                                      | Link
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----
Default config                                                                                                                                                                                   | [confgenerator/default-config.yaml](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/default-config.yaml) (Linux) and [confgenerator/windows-default-config.yaml](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/windows-default-config.yaml)(Windows)
Unified agent config generator. This handles the unified agent yaml reading and delegating subsections to the Open Telemetry Collector config translator and Fluent Bit config translator below. | [confgenerator/confgenerator.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/confgenerator.go) (implementation), [confgenerator/confgenerator_test.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/confgenerator_test.go) (unit tests), [confgenerator/testdata](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/testdata) (test data)
generate_config command implementation                                                                                                                                                           | [cmd/google_cloud_ops_agent_engine/main.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/cmd/google_cloud_ops_agent_engine/main.go) (Linux) and [cmd/ops_agent_windows/main_windows.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/cmd/google_cloud_ops_agent_engine/main.go) (Windows)
Open Telemetry Collector config translator                                                                                                                                                       | [otel/conf.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/otel/conf.go) (implementation) and [otel/conf_test.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/otel/conf_test.go) (unit tests)
Fluent Bit config translator                                                                                                                                                                     | [fluentbit/conf/conf.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/fluentbit/conf/conf.go) (implementation) and [fluentbit/conf/conf_test.go](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/fluentbit/conf/conf_test.go) (unit tests)

</details>

<details>
  <summary>Systemd related</summary>

Description                                                               | Link
------------------------------------------------------------------------- | ----
Configs for the `google-cloud-ops-agent` service                          | [systemd/google-cloud-ops-agent.service](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/systemd/google-cloud-ops-agent.service)
Configs for the `google-cloud-ops-agent-open-telemetry-collector` service | [systemd/google-cloud-ops-agent-opentelemetry-collector.service](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/systemd/google-cloud-ops-agent-opentelemetry-collector.service)
Configs for the `google-cloud-ops-agent-fluent-bit` service `<            | [systemd/google-cloud-ops-agent-fluent-bit.service](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/systemd/google-cloud-ops-agent-fluent-bit.service)

</details>

<details>
  <summary>Build related</summary>

Description                                                        | Link
------------------------------------------------------------------ | ----
Build container Dockerfile for Linux                               | [Dockerfile](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/Dockerfile)
Build container Dockerfile for Windows                             | [Dockerfile.windows](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/Dockerfile.windows)
Build script for a tarball                                         | [build.sh](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/build.sh)
Build script of the Deb packages for Debian and Ubuntu distros     | [pkg/deb/build.sh](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/pkg/deb/build.sh)
Build script of the RPM packages for CentOS, RHEL and Sles distros | [pkg/rpm/build.sh](https://github.com/GoogleCloudPlatform/ops-agent/blob/master/pkg/rpm/build.sh)
Build script of the Windows packages for Windows distros           | [pkg/goo/build.ps1](https://github.com/GoogleCloudPlatform/ops-agent/blob/master/pkg/goo/build.ps1)

</details>

## Check out code

Follow this workflow to check out the code from the repo:

```shell
$ git clone --recurse-submodules git@github.com:GoogleCloudPlatform/ops-agent.git
$ cd ops-agent
```

> **Tip:** After you make changes to the code base and run unit tests, in case
> the golden files are updated, the following command can be used to see the
> diff easily that excludes all golden files. This is helpful if you are doing
> PR code reviews by checking out the code locally too, because GitHub does not
> have a good way to easily see all the files that are changed.

```shell
$ git diff origin/master -- . ':!confgenerator/testdata'
```

## Run goimports

Run `goimports` to keep the codebase format style in sync:

```shell
ops-agent$ goimports -w .
```

## Test locally

### Run unit tests

#### Run all unit tests

```shell
ops-agent$ go test -mod=mod ./...
```

#### Only run unified agent config generator tests

```shell
ops-agent$ go test -mod=mod github.com/GoogleCloudPlatform/ops-agent/confgenerator
```

In case the failed diff is indeed expected, you can bulk update the golden
Fluent Bit and Open Telemetry Collector conf files in the
`confgenerator/testdata/valid` folder by:

```shell
ops-agent$ go test -mod=mod github.com/GoogleCloudPlatform/ops-agent/confgenerator -update_golden
```

Add "-v" to show details for which files are updated with what:

```shell
ops-agent$ go test -mod=mod github.com/GoogleCloudPlatform/ops-agent/confgenerator -update_golden -v
```

*   Understanding the config generator tests

    In each
    [test data](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/testdata/),
    `input.yaml` is the input, which is the Ops Agent YAML config file.
    `*_fluent_bit_*.conf` are the generated Fluent Bit configuration files.

    [public documentation](https://cloud.google.com/stackdriver/docs/solutions/ops-agent/configuration)
    that will have the official config syntax.

    The
    [config generator](https://github.com/GoogleCloudPlatform/ops-agent/tree/master/confgenerator/confgenerator.go)
    uses https://github.com/go-yaml/yaml for basic YAML validations. It uses
    https://golang.org/pkg/text/template/ for templating the configs.

#### Only run Fluent Bit config translator tests

```shell
ops-agent$ go test -mod=mod github.com/GoogleCloudPlatform/ops-agent/fluentbit/conf
```

#### Only run Open Telemetry Collector config translator tests

```shell
ops-agent$ go test -mod=mod github.com/GoogleCloudPlatform/ops-agent/otel
```

### Test config generation manually

Config generation can be triggered manually via the `generate_config` command
for development.

```shell
$ export CONFIG_IN=confgenerator/default-config.yaml  # Ops Agent config path
$ export CONFIG_OUT=tmp/google-cloud-ops-agent/conf   # Output directory to write configs to

$ mkdir -p $CONFIG_OUT
ops-agent$ go run -mod=mod cmd/google_cloud_ops_agent_engine/main.go \
  --service=fluentbit \
  --in=$CONFIG_IN \
  --out=$CONFIG_OUT
ops-agent$ go run -mod=mod cmd/google_cloud_ops_agent_engine/main.go \
  --service=otel \
  --in=$CONFIG_IN \
  --out=$CONFIG_OUT
$ tree $CONFIG_OUT
```

*   Sample generated
    [golden fluent bit main conf](https://github.com/GoogleCloudPlatform/ops-agent/blob/master/confgenerator/testdata/valid/linux/default_config/golden_fluent_bit_main.conf)
    at `$CONFIG_OUT/fluent_bit_main.conf`.
*   Sample generated
    [golden fluent bit parser conf](https://github.com/GoogleCloudPlatform/ops-agent/blob/master/confgenerator/testdata/valid/linux/default_config/golden_fluent_bit_parser.conf)
    at `$CONFIG_OUT/fluent_bit_parser.conf`.
*   Sample generated
    [golden otel conf](https://github.com/GoogleCloudPlatform/ops-agent/blob/master/confgenerator/testdata/valid/linux/default_config/golden_otel.conf)
    at `$CONFIG_OUT/otel.conf`.

## Build and test automatically on GCE VMs

### Testing changes from a GitHub dev branch

1.  Check out the scripts.

    Note: This will clean up your local `/tmp/google-cloud-ops-agent/` repo.

    Note: Here we use GitHub instead of Git-on-borg because the sync between the
    two can take > 10 minutes and cause delay for development.

    ```shell
    # Your dev branch name or the commit hash, if it's not master
    $ export GIT_BRANCH=

    # Adjust the GitHub repo owner if you are testing from a fork
    $ export GITHUB_REPO_OWNER=GoogleCloudPlatform

    $ rm -rf /tmp/google-cloud-ops-agent/
    $ DATETIME=$(date +'%Y%m%d-%H%M%S')
    $ g4d -f {{USERNAME}}-release-ops-agent-$DATETIME
    $ cd cloud/monitoring/agents/release_scripts/ops_agent
    $ export USE_GITHUB=1
    $ export GITHUB_REPO_NAME=ops-agent
    ```

1.  Trigger the build and test jobs.

    To build and test for all platforms, use:

    ```shell
    $ ./build_and_test_all.sh $GIT_BRANCH
    ```

    To build and test a single distro, set `$DISTRO` to one of the following
    values:

    -   sles12
    -   sles15
    -   stretch
    -   buster
    -   xenial
    -   bionic
    -   focal
    -   centos7
    -   centos8
    -   windows

    Then run:

    ```shell
    ./build_and_test.sh $DISTRO $GIT_BRANCH
    ```

    You can check the status (pass/fail) of all distros by running:

    ```bash
    ./status.sh
    ```

    <details>
      <summary>Retry and troubleshooting:</summary>

    If certain distros failed the build, and you suspect it's a flake, rerun
    that distro by:

    ```bash
      ./build.sh $DISTRO
    ```

    If certain distros failed, and you suspect it's a flake, rerun that distro
    by

    ```bash
      ./test.sh $DISTRO
    ```

    or rerun all tests with the built packages:

    ```bash
      ./test_all.sh
    ```

    then check with `./status.sh` again.

    </details>
