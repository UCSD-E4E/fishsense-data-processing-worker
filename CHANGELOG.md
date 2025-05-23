# CHANGELOG


## v0.4.4 (2025-04-16)

### Bug Fixes

- Adds backoff for downloading
  ([`106f725`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/106f7255e0c9356fd580c3c55178689c99e9acc6))


## v0.4.3 (2025-04-15)

### Bug Fixes

- Adds sleep for no job
  ([`b9ab587`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/b9ab587ac42b2804dca6e4b1e888582cd32033fc))


## v0.4.2 (2025-04-15)

### Bug Fixes

- Updates job fail behavior
  ([`6ca3d38`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/6ca3d3886600871bfc339615e02c4d5da8eabc28))

### Chores

- Adds k8s tooling
  ([`d03ee90`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/d03ee9087bab630210042751f5b081013e19a7bd))

### Continuous Integration

- Updates deploy
  ([`9440349`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/9440349ccdabc6bef803cb564331a52ffbf73ca4))


## v0.4.1 (2025-04-15)

### Bug Fixes

- Adds bailout to session.put
  ([`be549fa`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/be549fac6923da7b6dbabe0a0a9ec8f4e14da69e))

### Continuous Integration

- Increases batch size
  ([`82ada45`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/82ada450d0b7c1cffce24eb9527e08fb93028758))

- Increases batch size to 300
  ([`8cf26a4`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/8cf26a4bc36f53b73cd210cc52a7dadbeca89c31))

- Increases batch size to 450
  ([`1c45026`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/1c450261ef74fa5ead1e5beae1ff681aa2f3a9ce))

- Updates deploy
  ([`3424d4e`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/3424d4ea9523d532538d6000a54f2a36e5ba4438))

- Updates resources requests
  ([`8eeef4b`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/8eeef4b1a59400451df71e09cd52f288db238001))


## v0.4.0 (2025-04-13)

### Features

- Adds batch size as env var
  ([`5b82d27`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/5b82d27401a5e606b6deb17795f433af3939290b))


## v0.3.2 (2025-04-13)

### Bug Fixes

- Fixes downloader CPU count
  ([`2e60b2b`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/2e60b2bfd13f22c59ef4c6400e976a5a22460656))

### Continuous Integration

- Upgrade image
  ([`cbd7728`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/cbd7728ba2019f36ff083d691e114a519f7f6761))


## v0.3.1 (2025-04-13)

### Bug Fixes

- Removes builtin ray config
  ([`562fc47`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/562fc476b687cb895e4e468de8d68666b8933178))


## v0.3.0 (2025-04-13)


## v0.2.6 (2025-04-13)

### Bug Fixes

- Fixes worker name
  ([`cec80ba`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/cec80ba98cba2ce07a5e45c168f33ddab085a781))

### Continuous Integration

- Adds secret and worker
  ([`1acd1a2`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/1acd1a27ef316ab41d4559d55da2c1c155324cd4))

### Features

- Allows env set of ray config
  ([`1563a59`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/1563a594bfaac67f6685c320ffa5a84b95bb95cb))


## v0.2.5 (2025-04-12)

### Bug Fixes

- Adds container env
  ([`bf20794`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/bf207942a6af7f102d611eef05e97800e89faefa))

- Adds CUDA driver affinity
  ([`cf20587`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/cf20587b91200a5447a589f13147a3fff6f0f231))

- Fixes ownership
  ([`861ae1f`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/861ae1f66a694878810e3b3046e681b219631e29))

- Switches to latest label
  ([`526ee5f`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/526ee5f04f2fd57556c2b34c5abc4c259a45e8e9))

### Chores

- Initial k8s deploy
  ([`1461724`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/1461724294161bede04fbb46d3b9453a82ff9a2e))

- Removes unused settings
  ([`2fedf64`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/2fedf6400910f022509dcc827a3c6bc5cc3b6327))

### Continuous Integration

- Switching to version label
  ([`4d0c11b`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/4d0c11b3a02118c6f8c74aaccc78afd888679e3c))


## v0.2.4 (2025-04-12)

### Bug Fixes

- Updates dockerfile
  ([`ddb34c5`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/ddb34c55af9fb0cec2d929bc7aac9a52f3a72eaf))


## v0.2.3 (2025-04-12)


## v0.2.2 (2025-04-12)

### Bug Fixes

- Fixes build
  ([`d75d376`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/d75d376cc70ab23d35fe124046f424cb199d941c))

- Fixes build from fishsense-docker
  ([`4bd833a`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/4bd833a5a152bbde7abe66b8d7de461103e19795))

### Continuous Integration

- Fixes only on branches
  ([`a1cc0ae`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/a1cc0ae23881dda0bf7e6f304470dcbdca84f681))


## v0.2.1 (2025-04-11)

### Bug Fixes

- Force version bump
  ([`5a4fcb0`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/5a4fcb0f696cccb3d2983f1a3ea8e71401ea9059))

### Code Style

- Fixing style issues
  ([`21af88c`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/21af88ca0c87a432c9daee54d88e46acb6b55234))

### Continuous Integration

- Adds docker build
  ([`944746a`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/944746a1d192544f41f171b21afe20c5f97e051b))

- Prunes garbage
  ([`ed2fcc8`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/ed2fcc887512669379acd8be66b9d612f3902499))


## v0.2.0 (2025-04-11)

### Bug Fixes

- Adds cache disallow for git fishsense-lite
  ([`75ee9f1`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/75ee9f16d95a9154648a358cd486fcc658657599))

- Adds modifiable suffix
  ([`66dd8b1`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/66dd8b1fe6ec9f131766e2690c2d34172ed8ea1b))

- Deploy to HTTPS
  ([`fbf879d`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/fbf879d8fd8c528814bfd95359b9ed88cd6a41d9))

- Dumps cache
  ([`2807c5d`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/2807c5d60088c9b313e933900e8bd1104b857574))

- Fixes Dockerfile caching
  ([`45d6142`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/45d614229f56b9ea37f5df4a3b4cf898fb5ee649))

- Fixes host
  ([`9d8ed5f`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/9d8ed5ff0b126921317075e2a0a5a0f56b4f1cb5))

- Fixes termination signal
  ([`e2e97be`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/e2e97be1fbeacf7d4faab7fd727dd6fc61128ae8))

### Code Style

- Removes unused import
  ([`08e53c5`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/08e53c53fbb4855049ef8cd6d9953c04b67e0b7d))

### Features

- Adds fsl_lite
  ([`01f54c6`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/01f54c655ad2fc3d26198d187ac8bb13dccd3d22))

- Adds initial endpoint definition
  ([`324d8cc`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/324d8cc28af07a678e5bb471cb563b199507c70f))

- Adds instrumentation
  ([`01f2045`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/01f20452edd1c80eded32bfd9002395710e049a1))

- Adds preprocess_with_laser
  ([`5adf299`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/5adf29983b857dffbec5188af89e1c9cc55c29af))

- Adds processing structure
  ([`09bd838`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/09bd8387c5b3e07a57441503f7108dee65dd5429))

- Closes job loop
  ([`b1033e5`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/b1033e5e3bba1e3c575f54412378e7114123ce66))

- Completes handler
  ([`0e62493`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/0e62493bfd9a986b6188b6754301b80959edbe73))

- Enables initial preprocess
  ([`3d97de0`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/3d97de07d377d104d6e04d3f5b532298d1051850))

- Handling output files
  ([`0c644a1`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/0c644a1cdc0f2d8e20bcfc0f6e923a0f7f9103b7))

- Increases resource limits
  ([`486ce8f`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/486ce8f7c3257e17c59f977fb6dc6215c4e8619e))


## v0.1.0 (2025-03-17)

### Bug Fixes

- Adds logging
  ([`ae1f61e`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/ae1f61e73dfe5cb47dce9737332e49c88d8d4ee1))

### Code Style

- Fixes pylint errors
  ([`0574a06`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/0574a06d8b3d3469aa5166a73f10e37becee7df4))

### Continuous Integration

- Adds dummy test
  ([`80f504a`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/80f504ad32da78d5e8c84dd2155b4531f4a83e73))

- Renames test.py
  ([`dd17391`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/dd173910c8ea4e5adeca293eb0cfd552769c779d))

### Documentation

- Fixes readme
  ([`d4b0105`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/d4b0105c3fd94c6ea8a0d50619d4c0293c80e579))

### Features

- Initial operating capability
  ([`d7316c2`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/d7316c25bbcdc1f0116fef9d09a872df24ef5f13))

- Initial structure
  ([`928b275`](https://github.com/UCSD-E4E/fishsense-data-processing-worker/commit/928b27586993c60b1c794f88eccfe135204a002a))
