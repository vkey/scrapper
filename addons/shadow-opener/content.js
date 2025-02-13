const script = document.createElement('script');
script.src = chrome.runtime.getURL('inject.js');
document.documentElement.prepend(script);
document.documentElement.append(script);
