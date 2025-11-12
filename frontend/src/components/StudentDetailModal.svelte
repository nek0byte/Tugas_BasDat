<script>
  import { createEventDispatcher, onMount } from "svelte";

  export let student = null;
  export let open = false;

  const dispatch = createEventDispatcher();

  function close() {
    dispatch("close");
  }

  function handleBackdrop(event) {
    if (event.target === event.currentTarget) {
      close();
    }
  }

  onMount(() => {
    function onKey(event) {
      if (event.key === "Escape") {
        close();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });
</script>

{#if open && student}
  <div
    class="fixed inset-0 z-40 flex items-center justify-center bg-slate-950/70 backdrop-blur-sm"
    on:click={handleBackdrop}
  >
    <div class="relative w-full max-w-md rounded-2xl bg-slate-900 p-6 shadow-xl">
      <button
        class="absolute right-4 top-4 text-slate-400 transition hover:text-slate-200"
        type="button"
        on:click={close}
        aria-label="Close modal"
      >
        ✕
      </button>
      <header class="mb-4">
        <h2 class="text-2xl font-bold text-slate-100">{student.name}</h2>
        <p class="text-sm text-slate-400">NIM: {student.nim}</p>
      </header>
      <section class="space-y-3 text-sm text-slate-200">
        <p><span class="text-slate-400">Program Studi:</span> {student.program_studi || "—"}</p>
        <p><span class="text-slate-400">Angkatan:</span> {student.angkatan || "—"}</p>
        <p><span class="text-slate-400">IPK:</span> {student.ipk ?? "—"}</p>
        <p><span class="text-slate-400">Email:</span> {student.email || "—"}</p>
        <p><span class="text-slate-400">Phone:</span> {student.phone || "—"}</p>
      </section>
      <footer class="mt-6 flex justify-end">
        <button
          class="rounded-lg bg-brand px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-dark"
          type="button"
          on:click={close}
        >
          Close
        </button>
      </footer>
    </div>
  </div>
{/if}

