module.exports = {
  root: true,
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module"
  },
  env: {
    browser: true,
    es2021: true
  },
  extends: ["eslint:recommended", "plugin:svelte/recommended"],
  overrides: [
    {
      files: ["*.svelte"],
      processor: "svelte/svelte"
    }
  ],
  ignorePatterns: ["dist"]
};

