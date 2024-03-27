import { versionRegExp } from 'ember-cli-app-version/utils/regexp';

import config from 'outdated/config/environment';

const appVersion = () => config.APP.version.match(versionRegExp);

export default appVersion;
