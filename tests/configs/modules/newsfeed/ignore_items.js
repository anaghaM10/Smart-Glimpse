/* Smart Glimpse Test config newsfeed module
 *
 * MIT Licensed.
 */
let config = {
	timeFormat: 12,

	modules: [
		{
			module: "newsfeed",
			position: "bottom_bar",
			config: {
				feeds: [
					{
						title: "Rodrigo Ramirez Blog",
						url: "http://localhost:8080/tests/mocks/newsfeed_test.xml"
					}
				],
				ignoreOldItems: true
			}
		}
	]
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {
	module.exports = config;
}
