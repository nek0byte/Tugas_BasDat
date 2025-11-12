<script>
  import { onDestroy, onMount } from "svelte";
  import SearchBar from "./components/SearchBar.svelte";
  import StudentCard from "./components/StudentCard.svelte";
  import StudentDetailModal from "./components/StudentDetailModal.svelte";
  import { fetchStudents, syncStudents } from "./lib/api";

  let students = [];
  let loading = false;
  let syncing = false;
  let searchQuery = "";
  let selectedStudent = null;
  let detailOpen = false;
  let toast = null;

  let searchTimer;

  async function loadStudents({ query = searchQuery } = {}) {
    loading = true;
    try {
      students = await fetchStudents({ search: query });
    } catch (error) {
      console.error(error);
      showToast("Failed to load students", "error");
    } finally {
      loading = false;
    }
  }

  function showToast(message, variant = "info") {
    toast = { message, variant };
    setTimeout(() => {
      toast = null;
    }, 4000);
  }

  function handleSearchChange(event) {
    searchQuery = event.detail;
    if (searchTimer) {
      clearTimeout(searchTimer);
    }
    searchTimer = setTimeout(() => {
      loadStudents({ query: searchQuery });
    }, 300);
  }

  function handleSearchClear() {
    searchQuery = "";
    loadStudents({ query: "" });
  }

  async function handleSync() {
    syncing = true;
    try {
      const response = await syncStudents();
      showToast(`Sync success. Imported ${response.stats.created} new, ${response.stats.updated} updated.`);
      await loadStudents();
    } catch (error) {
      console.error(error);
      showToast("Sync failed. Check server logs.", "error");
    } finally {
      syncing = false;
    }
  }

  function openDetail(student) {
    selectedStudent = student;
    detailOpen = true;
  }

  function closeDetail() {
    detailOpen = false;
  }

  onMount(() => {
    loadStudents();
  });

  onDestroy(() => {
    if (searchTimer) {
      clearTimeout(searchTimer);
    }
  });
</script>

<main class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100">
  <div class="mx-auto flex w-full max-w-6xl flex-col gap-8 px-6 py-10">
    <header class="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
      <div>
        <h1 class="text-3xl font-bold tracking-tight text-white md:text-4xl">Student Dashboard</h1>
        <p class="mt-2 text-sm text-slate-400">
          Explore student data, search by name, and trigger data sync from the backend.
        </p>
      </div>
      <button
        class="inline-flex items-center gap-2 rounded-lg bg-brand px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-dark disabled:cursor-not-allowed disabled:bg-slate-700"
        type="button"
        on:click={handleSync}
        disabled={syncing}
      >
        {#if syncing}
          <span class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
          Syncing…
        {:else}
          <span class="h-2 w-2 rounded-full bg-brand-light shadow shadow-brand-light"></span>
          Sync Data
        {/if}
      </button>
    </header>

    <section class="flex flex-col gap-6">
      <SearchBar
        value={searchQuery}
        on:change={handleSearchChange}
        on:clear={handleSearchClear}
      />
      {#if toast}
        <div
          class={`flex items-center justify-between rounded-xl border px-4 py-3 text-sm shadow ${
            toast.variant === "error"
              ? "border-red-500/40 bg-red-500/10 text-red-200"
              : "border-emerald-500/40 bg-emerald-500/10 text-emerald-200"
          }`}
        >
          <span>{toast.message}</span>
        </div>
      {/if}
    </section>

    <section>
      {#if loading}
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
          {#each Array(6) as _, index}
            <div
              class="h-48 animate-pulse rounded-xl bg-slate-800/60"
              aria-label={`Loading placeholder ${index + 1}`}
            />
          {/each}
        </div>
      {:else if students.length === 0}
        <div class="rounded-xl border border-slate-800 bg-slate-900/60 p-8 text-center text-slate-400">
          No students found. Try adjusting your search or sync the data.
        </div>
      {:else}
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
          {#each students as student (student.id)}
            <StudentCard student={student} on:select={() => openDetail(student)} />
          {/each}
        </div>
      {/if}
    </section>
  </div>

  <StudentDetailModal student={selectedStudent} open={detailOpen} on:close={closeDetail} />
</main>

