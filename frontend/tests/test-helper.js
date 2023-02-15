import { setApplication } from '@ember/test-helpers';
import { start } from 'ember-qunit';
import Application from 'outdated/app';
import config from 'outdated/config/environment';
import * as QUnit from 'qunit';
import { setup } from 'qunit-dom';

setApplication(Application.create(config.APP));

setup(QUnit.assert);

start();
