public BlockingInterface getProxy()
    throws IOException {
    if (proxy == null) {
        proxy = createProxy();
    }
    return proxy;
}