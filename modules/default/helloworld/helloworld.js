/* Smart Glimpse
 * Module: HelloWorld
 *
 */

Module.register("helloworld", {
	// Default module config.
	defaults: {
		text: "Hello World!"
	},
	path: "C:\Users\hp\Desktop\emotion detection\emotion3",
	getTemplate () {
		return "helloworld.njk";
	},

	async start(){
		console.log('Hello world path:'+ this.path)
		
	},
	getTemplateData () {
		return this.config;
	}
});
