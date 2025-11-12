<script>
  import { createEventDispatcher } from "svelte";

  export let value = "";
  export let placeholder = "Search by name...";

  const dispatch = createEventDispatcher();

  function handleInput(event) {
    dispatch("change", event.target.value);
  }

  function clear() {
    value = "";
    dispatch("clear");
  }
</script>

<div class="flex items-center gap-3 rounded-lg bg-slate-800 px-4 py-3 shadow">
  <input
    class="w-full bg-transparent text-sm text-slate-100 placeholder:text-slate-400 focus:outline-none"
    type="search"
    bind:value
    on:input={handleInput}
    placeholder={placeholder}
  />
  {#if value}
    <button
      type="button"
      class="rounded-md bg-slate-700 px-3 py-1 text-xs font-semibold text-slate-200 hover:bg-slate-600 transition"
      on:click={clear}
    >
      Clear
    </button>
  {/if}
</div>

