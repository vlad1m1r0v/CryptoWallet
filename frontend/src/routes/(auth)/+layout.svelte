<script lang="ts">
    let {children} = $props();
</script>

<svelte:head>
    <!-- BEGIN: Page CSS-->
    <link rel="stylesheet" type="text/css" href="vuexy/css/plugins/forms/form-validation.css">
    <link rel="stylesheet" type="text/css" href="vuexy/css/pages/page-auth.css">
    <!-- END: Page CSS-->
    <title>Authentication</title>
</svelte:head>

<div class="content-overlay"></div>
<div class="content-wrapper">
    <div class="content-header row">
    </div>
    <div class="content-body">
        <div class="auth-wrapper auth-v1 px-2">
            <div class="auth-inner py-2">
                <!-- Login v1 -->
                <div class="card mb-0">
                    <div class="card-body">
                        {@render children?.()}
                    </div>
                </div>
                <!-- /Login v1 -->
            </div>
        </div>

    </div>
</div>