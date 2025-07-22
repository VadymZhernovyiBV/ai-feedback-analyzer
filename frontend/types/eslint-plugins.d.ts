declare module 'eslint-plugin-react-hooks'
declare module 'eslint-plugin-react-refresh' {
  const plugin: {
    configs: {
      recommended: {
        rules: Record<string, unknown>
      }
    }
  }
  export default plugin
}