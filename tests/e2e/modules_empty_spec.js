const helpers = require("./helpers/global-setup");

describe("Check configuration without modules", () => {
	beforeAll(async () => {
		await helpers.startApplication("tests/configs/without_modules.js");
		await helpers.getDocument();
	});
	afterAll(async () => {
		await helpers.stopApplication();
	});

	it("shows the message Smart Glimpse title", async () => {
		const elem = await helpers.waitForElement("#module_1_helloworld .module-content");
		expect(elem).not.toBeNull();
		expect(elem.textContent).toContain("Smart Glimpse");
	});

	it("shows the url of michael's website", async () => {
		const elem = await helpers.waitForElement("#module_5_helloworld .module-content");
		expect(elem).not.toBeNull();
		expect(elem.textContent).toContain("www.michaelteeuw.nl");
	});
});
