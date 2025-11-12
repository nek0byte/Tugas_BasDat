<script>
  import { createEventDispatcher } from "svelte";

  export let student;

  const dispatch = createEventDispatcher();

  function openDetail() {
    dispatch("select", student);
  }
</script>

<article
  class="group flex flex-col justify-between rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow transition hover:-translate-y-1 hover:border-brand hover:bg-slate-800/80"
>
  <header class="mb-3">
    <h3 class="text-lg font-semibold text-slate-100 group-hover:text-brand-light transition">
      {student.name}
    </h3>
    <p class="text-xs uppercase tracking-wide text-slate-400">NIM: {student.nim}</p>
  </header>

  <dl class="grid grid-cols-2 gap-2 text-sm text-slate-300">
    <div>
      <dt class="text-xs text-slate-500">Program Studi</dt>
      <dd>{student.program_studi || "—"}</dd>
    </div>
    <div>
      <dt class="text-xs text-slate-500">Angkatan</dt>
      <dd>{student.angkatan || "—"}</dd>
    </div>
    <div>
      <dt class="text-xs text-slate-500">IPK</dt>
      <dd>{student.ipk ?? "—"}</dd>
    </div>
    <div>
      <dt class="text-xs text-slate-500">Email</dt>
      <dd class="truncate">{student.email || "—"}</dd>
    </div>
  </dl>

  <button
    type="button"
    class="mt-4 inline-flex items-center justify-center rounded-lg bg-brand px-4 py-2 text-sm font-semibold text-white transition hover:bg-brand-dark focus:outline-none focus:ring-2 focus:ring-brand-light focus:ring-offset-2 focus:ring-offset-slate-900"
    on:click={openDetail}
  >
    View Detail
  </button>
</article>

