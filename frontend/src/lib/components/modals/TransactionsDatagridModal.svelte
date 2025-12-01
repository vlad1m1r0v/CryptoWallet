<style>
    #container {
        display: grid;
        height: calc(100vh - 200px);
        grid-template-areas: "grid" "paginator";
        gap: 10px;
        grid-template-rows: 1fr max(25px, fitcontent);
        align-items: center;
    }

    #container #grid {
        grid-area: grid;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    #container #paginator {
        grid-area: paginator;
        overflow-x: auto;
    }

    #container {
        --wx-table-header-background: #ffffff;
        --wx-table-cell-border: 1px solid #e6e6e6;
        --wx-table-header-border: 1px solid #e6e6e6;
    }
</style>
<script lang="ts">
    const {
        isOpen,
        close,
        walletAddress,
        walletId
    }: {
        isOpen: boolean,
        close: () => {},
        walletAddress: string,
        walletId: string,
    } = $props();
    import {Willow, Pager} from "@svar-ui/svelte-core";
    import {Grid} from "@svar-ui/svelte-grid";

    import {fade, scale} from "svelte/transition";

    const data = [
        {
            "id": "019ad621-d0b9-76b8-bf94-6a4b7452c0ca",
            "transaction_hash": "0x4d723a2b2f9472d14a65e6ed18af86edeefb226c2149cb6480421202d9303953",
            "from_address": "0x9a0c272bd8bb40edb2689bf48b395f8ecb561d55",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "0.00002053843092",
            "transaction_status": "successful",
            "created_at": "2025-09-16T15:34:48Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0ba-7f11-813d-f68bbe0bbb84",
            "transaction_hash": "0x0c97728ace5f9bb3c85ab72900bc35c25f4a11648015d5e018d80db4010ace68",
            "from_address": "0xfda8452066a0b78dcf6c10dcd988bf18cb19d3f5",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.06",
            "transaction_fee": "4.36921842E-7",
            "transaction_status": "successful",
            "created_at": "2025-09-16T16:02:24Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0bb-7407-b9f6-2f3b50aa2584",
            "transaction_hash": "0xc7bbd36abee1a011e87c239c871e71fcd96e0de38a9e0a8431cb4d0c9c593993",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T22:39:24Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0bc-784c-91fd-feafe0d0d1f1",
            "transaction_hash": "0xbe1c0daf4199ff6eb2036ffbeb13d7f6a737c017ccf68f516799f6294d9e92d2",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T22:40:24Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0bd-7aa0-897c-033c93f42de3",
            "transaction_hash": "0xb043d75f599e679c7b8d794867b1f310c7da408c1b59c1f1dea092686ed0d94f",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T22:41:36Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0be-75a4-a74a-3e69339a8687",
            "transaction_hash": "0x967da7fb1df6bd3d3443b58f90cbe2e2902455d07503f20492bff1dbc2c3813a",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T22:42:24Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0bf-78a1-98a8-a9036451252e",
            "transaction_hash": "0x6a52281d10d4e2f2ccf9f63f5e8d911bb9a8f77218860b061da4b6e18ccc0b95",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T23:04:00Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c0-7212-af00-803c6aa2a41a",
            "transaction_hash": "0x1cdb2bcad027d565d49ead2579f6aa71b3cf2aade3da050bb5e851d6ed73913c",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T23:19:36Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c1-7137-a6a6-c16a9f1e8144",
            "transaction_hash": "0x721a1be7f8a3263c22abf5b18d0bf4fb32bf583b7cbb3f7f28a5ff90daeb6c96",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T23:20:24Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c2-7e25-a1dc-9c7c80122286",
            "transaction_hash": "0xad6e365761b0ac094fb36eee00c7d11b24008781259fd17a012b1a1bead8d985",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-16T23:25:00Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c3-7701-90d4-56a250eba2e3",
            "transaction_hash": "0x50194142c731fc50dd1af1b93f6156be5a1af9fe1e8ecf8e981ca6ae4b054ad8",
            "from_address": "0x42645ce4dd0b766de53ee483cbf54bcea670f9b2",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "8.5449105E-7",
            "transaction_status": "successful",
            "created_at": "2025-09-17T18:10:00Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c4-765c-9c57-bf7150051002",
            "transaction_hash": "0x978cd5012bfb653b2b1ced7b8d03e03891e3cbebc9421b454562acdf9693ccf9",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-09-17T18:29:12Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c5-7d77-96b0-12fea5b6f36e",
            "transaction_hash": "0x2818888ca298260dd3dd84249a386a81d3cd7e35213277a3254badb2ec6b26c9",
            "from_address": "0xb2de751d22adfb449e95da3c1e8836c6c61b537d",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "6.9322743E-7",
            "transaction_status": "successful",
            "created_at": "2025-09-19T20:30:24Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c6-7252-81ac-945e76edd177",
            "transaction_hash": "0x99179fc674e1b99012fb1d514f783057d8b08db2d9a3c5c8a70b6158bc762a84",
            "from_address": "0xfda8452066a0b78dcf6c10dcd988bf18cb19d3f5",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.06",
            "transaction_fee": "2.1226947E-8",
            "transaction_status": "successful",
            "created_at": "2025-09-20T12:10:12Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c7-7285-9ccb-dbb37e72d1f7",
            "transaction_hash": "0xb7be407a0e6351e90c6788832d0a43844d347602fe844e2300697613714b1b47",
            "from_address": "0x15095ec8fb1fc9c664b3223459dff43158ace7ad",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "7.0070364E-7",
            "transaction_status": "successful",
            "created_at": "2025-09-22T11:54:00Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c8-7fdb-9bc4-33b938339936",
            "transaction_hash": "0xc274ffc4019f914c3682a43891288f3cee2aed99ad720ec54558236d25beda21",
            "from_address": "0x6efb29cee3b414272eb7a8f3ebabf873d36bc033",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "6.9301575E-7",
            "transaction_status": "successful",
            "created_at": "2025-10-05T22:32:48Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0c9-75fe-83b1-eaa4eee90231",
            "transaction_hash": "0xd781d448105e45b98f814e862da5de12c9e22d116d6cb26b90da6c641b6c4c7f",
            "from_address": "0x9a0c272bd8bb40edb2689bf48b395f8ecb561d55",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "6.9302331E-7",
            "transaction_status": "successful",
            "created_at": "2025-10-10T17:21:12Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0ca-7c55-baae-7f8aa2c4c3d4",
            "transaction_hash": "0xb8974030ee96a2d446efbcffb031c0ac61daf2b8b80a8a1e46643d38c501fe15",
            "from_address": "0x15095ec8fb1fc9c664b3223459dff43158ace7ad",
            "to_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "value": "0.05",
            "transaction_fee": "6.930063E-7",
            "transaction_status": "successful",
            "created_at": "2025-10-27T11:02:00Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0cb-7475-b379-0b24f97e56cf",
            "transaction_hash": "0xc2b3876559fd5eef40b06ccbb7fea0cc99612a6f9677508c7d2de7f77eae45c9",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "1.05E-7",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-10-27T14:32:36Z",
            "asset_symbol": "ETH"
        },
        {
            "id": "019ad621-d0cc-7728-acb6-e08e220f4ec1",
            "transaction_hash": "0x006b0236c2beef0bd35f4c9e8ef7940255abaa8d639105df843d920b1a883794",
            "from_address": "0xf04555b42b45e5283f28737d6ba65ae16878d84b",
            "to_address": "0x502b48fb202786302d098e1078542abc5bfedd6c",
            "value": "0.001000105",
            "transaction_fee": "0.000105",
            "transaction_status": "successful",
            "created_at": "2025-10-27T14:37:48Z",
            "asset_symbol": "ETH"
        }
    ];

    const columns = [
        {
            id: "id",
            header: "ID",
            hidden: true,
        },
        {
            id: "transaction_hash",
            header: "Transaction Hash",
            width: 400
        },
        {
            id: "from_address",
            header: "From Address",
            width: 300
        },
        {
            id: "to_address",
            header: "To Address",
            width: 300
        },
        {
            id: "value",
            header: "Value",
            width: 150
        },
        {
            id: "transaction_fee",
            header: "Fee",
            width: 150,
            sort: true,
        },
        {
            id: "transaction_status",
            header: "Status",
            width: 100,
            sort: true,
        },
        {
            id: "created_at",
            header: "Date",
            width: 150,
            sort: true
        },
        {
            id: "asset_symbol",
            header: "Asset",
            width: 70
        }
    ];

    import {outsideClick} from "$lib/actions/outsideClick.ts";
</script>
{#if isOpen}
    <div
            class="modal d-block text-left modal-primary"
            transition:fade|global={{duration: 200}}
            style="z-index: 3000"
    >
        <div
                class="modal-dialog modal-dialog-centered modal-xl"
                role="document"
                transition:scale|global="{{ start: 0.8, duration: 200 }}"
        >
            <div
                    class="modal-content"
                    use:outsideClick
                    on:outsideclick={close}
            >
                <Willow>
                    <div class="modal-header">
                        <h5 class="modal-title text-truncate">Transactions history of wallet {walletAddress}</h5>
                        <button
                                type="button"
                                class="close"
                                data-dismiss="modal"
                                aria-label="Close"
                                on:click={close}
                        >
                            <span aria-hidden="true">×</span>
                        </button>
                    </div>
                    <div class="modal-body" id="container">
                        <div id="grid">
                            <Grid columns={columns} data={data}></Grid>
                        </div>
                        <div id="paginator">
                            <Pager value={2} total={40}></Pager>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="flex flex-row">
                            <button
                                    type="button"
                                    class="btn btn-flat-primary waves-effect waves-float waves-light"
                                    data-dismiss="modal"
                                    on:click={close}
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </Willow>
            </div>
        </div>
    </div>
{/if}