import { concat } from '@ember/helper';
import { LinkTo } from '@ember/routing';
import UkTooltip from 'ember-uikit/modifiers/uk-tooltip';

import appVersion from 'outdated/utils/app-version';

<template>
  <div
    class='navbar'
    uk-sticky='sel-target: .navbar-container; cls-active: uk-navbar-sticky'
  >
    <nav class='navbar-container' uk-navbar>
      <div class='uk-navbar-left'>
        <div class='uk-navbar-item uk-logo uk-visible@m'>
          <LinkTo
            {{UkTooltip (concat 'v' (appVersion))}}
            @route='projects'
            class='uk-link-reset'
          >
            Outdated
          </LinkTo>
        </div>

        <ul class='button-nav uk-hidden@m'>
          <li>
            <LinkTo
              @route='projects.index'
              @current-when='projects.index projects.detailed not-found'
              class='uk-hidden@m'
              {{UkTooltip (concat 'v' (appVersion)) offset=false}}
            >Outdated</LinkTo>
          </li>
        </ul>
      </div>
      <div class='uk-navbar-right'>
        <ul class='button-nav'>
          <li class='uk-visible@m'>
            <LinkTo
              @route='projects.index'
              @current-when='projects.index projects.detailed not-found'
            >Overview</LinkTo>
          </li>
          <li>
            <LinkTo @route='projects.add'>Add</LinkTo>
          </li>
          <li>
            <LinkTo @route='dependencies'>Dependencies</LinkTo>
          </li>
          <li>
            <LinkTo @route='versions'>Versions</LinkTo>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>
