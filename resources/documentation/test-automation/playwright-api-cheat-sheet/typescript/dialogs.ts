// @playwright/test 1.x — register the listener BEFORE the triggering action
page.on('dialog', async (dialog) => {
  console.log(dialog.type(), dialog.message());
  await dialog.accept();
  // await dialog.dismiss();
  // await dialog.accept('prompt text');
});
