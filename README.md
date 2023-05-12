# Actions
Cloudforet has 90+ repositories, **70 of which are for applications** and these repositories have github action workflows.<br>
Because of that, it's very difficult to handle one by one when you need to update or run a workflow.

To solve this problem, we created `Actions`.<br>

The diagram below shows the relationship between Actions and repositories.
```
diagram
```

## What does actions actually do?

`Actions` is a control tower that manages and deploys github action workflows for Cloudforet's core services.<br>
It can also bulk trigger these workflows when a new version of Cloudforet's core services needs to be released.

### Manage and deploy github action workflows for Cloudforet's core services.
**All workflows for Cloudforet's core services are managed and deployed in this repository.**<br>

We write the workflow according to our workflow policy and put it in the [workflows](./workflows/) directory of `Actions`.<br>
then these can be deployed into repository of Cloudforet's core services.

Use this features, our devops engineers can modify workflows and deploy in batches.

The diagram below shows the process for this feature.
```
diagram
```


*) If you want to see the `Actions` script that appears  in the diagram, see [here](./src).

### Bulk trigger workflows when a new version of Cloudforet's core services needs to be released.
When a new version of Cloudforet's core services is released, we need to trigger the workflow of each repository.<br>
To do this, we made workflow that can trigger workflows of each repository in `Actions`.<br>

See [Workflows](./.github/workflows) for details.