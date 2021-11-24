Object.defineProperty(window, 'navigator', {
    value: new Proxy(navigator, {
        has: (target, key) => (key === 'webdriver' ? false : key in target),
        get: (target, key) =>
            key === 'webdriver' ?
                undefined :
                typeof target[key] === 'function' ?
                    target[key].bind(target) :
                    target[key]
    })
});