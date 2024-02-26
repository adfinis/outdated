import Application from '@ember/application';
import { debug } from '@ember/debug';
import loadInitializers from 'ember-load-initializers';
import Resolver from 'ember-resolver';

import config from 'outdated/config/environment';

export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  Resolver = Resolver;
}

const version = config.APP.version;
debug('-------------------------------');
debug(`Outdated : ${version}`);
loadInitializers(App, config.modulePrefix);
