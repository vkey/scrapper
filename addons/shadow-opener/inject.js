(function() {
    'use strict';
    const originalAttachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function(options) {
        const modifiedOptions = {
            ...(options || {}),
            mode: 'open'
        };

        return originalAttachShadow.call(this, modifiedOptions);
    };
})();
