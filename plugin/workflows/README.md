## Naming rule
```
[EVENT] CONTENT
```

## Workflows
- [Push] Build Dev
    - EVENT
        - When code is pushed to master
    - CONTENT
        - Build code and push docker image to pyengine
        - (triggered by `[Push] Sync CI`)
- [Dispatch] Release
    - EVENT
        - When the workflow is manually triggered
    - ACTION
        - Build code and push docker image to pyengine and spaceone
- [Push] Sync CI
    - EVENT
        - When code is pushed to master
    - CONTENT
        - Get workflows from actions
        - (trigger `[Push] Build dev` or `[Dispatch] Release`)
- [Dispatch] Sync CI
    - EVENT
        - When code is pushed to master
    - CONTENT
        - Get workflows from actions
- [PR] Review (TODO)

## scenario
- Release: `[Dispatch] Release`
- Build Dev (CI): `[Push] Sync CI([Push] Build Dev)`
- Build Dev (CD): `[Push] Build Dev`
- Pull workflows: `[Dispatch] Sync CI`