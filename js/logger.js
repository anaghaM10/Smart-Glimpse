/* Smart Glimpse
 * Log
 *
 * This logger is very simple, but needs to be extended.
 * This system can eventually be used to push the log messages to an external target.
 *
 */
(function (root, factory) {
	if (typeof exports === "object") {
		if (process.env.JEST_WORKER_ID === undefined) {
			// add timestamps in front of log messages
			require("console-stamp")(console, {
				pattern: "yyyy-mm-dd HH:MM:ss.l",
				include: ["debug", "log", "info", "warn", "error"]
			});
		}
		// Node, CommonJS-like
		module.exports = factory(root.config);
	} else {
		// Browser globals (root is window)
		root.Log = factory(root.config);
	}
}(this, function (config) {
	let logLevel;
	let enableLog;
	if (typeof exports === "object") {
		// in nodejs and not running with jest
		enableLog = process.env.JEST_WORKER_ID === undefined;
	} else {
		// in browser and not running with jsdom
		enableLog = typeof window === "object" && window.name !== "jsdom";
	}

	if (enableLog) {
		logLevel = {
			debug: Function.prototype.bind.call(console.debug, console),
			log: Function.prototype.bind.call(console.log, console),
			info: Function.prototype.bind.call(console.info, console),
			warn: Function.prototype.bind.call(console.warn, console),
			error: Function.prototype.bind.call(console.error, console),
			group: Function.prototype.bind.call(console.group, console),
			groupCollapsed: Function.prototype.bind.call(console.groupCollapsed, console),
			groupEnd: Function.prototype.bind.call(console.groupEnd, console),
			time: Function.prototype.bind.call(console.time, console),
			timeEnd: Function.prototype.bind.call(console.timeEnd, console),
			timeStamp: Function.prototype.bind.call(console.timeStamp, console)
		};

		logLevel.setLogLevel = function (newLevel) {
			if (newLevel) {
				Object.keys(logLevel).forEach(function (key) {
					if (!newLevel.includes(key.toLocaleUpperCase())) {
						logLevel[key] = function () {};
					}
				});
			}
		};
	} else {
		logLevel = {
			debug () {},
			log () {},
			info () {},
			warn () {},
			error () {},
			group () {},
			groupCollapsed () {},
			groupEnd () {},
			time () {},
			timeEnd () {},
			timeStamp () {}
		};

		logLevel.setLogLevel = function () {};
	}

	return logLevel;
}));
