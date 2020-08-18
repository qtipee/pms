module.exports = {
    root: true,
    env: {
        browser: true,
        node: true
    },
    parserOptions: {
        parser: 'babel-eslint'
    },
    extends: [
        '@nuxtjs',
        'plugin:nuxt/recommended'
    ],
    plugins: [
    ],
    // add your custom rules here
    rules: {
        semi: ['error', 'never'],
        indent: ['error', 4],
        'no-console': 2,
        'no-alert': 2,
        'no-debugger': 2,
        'vue/html-indent': ['error', 4],
        'vue/script-indent': ['error', 4]
    }
}
