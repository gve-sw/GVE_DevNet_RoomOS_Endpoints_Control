import xapi from 'xapi';

xapi.event.on('UserInterface Extensions Panel Clicked', (event) => {
  switch (event.PanelId) {
    case 'proUSB_Inactive_1-0-0':
      console.log('USB Mode Enabled, reconfigurring endpoint...')
      console.log('USB Mode configuration complete!')
      break;
    case 'proUSB_Active_1-0-0':
      console.log('USB Mode Disabled, restoring endpoint configuration...')
      xapi.Command.UserInterface.Message.Alert.Display
    ({ Duration: 4, Text: "USB Passthru mode on", Title: "USB Mode"});
      console.log('Default configuration restoration complete!')
      break;
    default:
      break;
  }
})