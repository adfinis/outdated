import { hash } from '@ember/helper';
import UkModal from 'ember-uikit/components/uk-modal';
import Body from 'ember-uikit/components/uk-modal/body';
import Footer from 'ember-uikit/components/uk-modal/footer';

<template>
  <UkModal
    @visible={{@visible}}
    @bgClose={{false}}
    @escClose={{false}}
    @btnClose={{false}}
    as |modal|
  >
    <modal.header>
      <h2 class='uk-modal-title'>{{@title}}</h2>
    </modal.header>
    {{#if @visible}}
      {{yield (hash body=(component Body) footer=(component Footer))}}
    {{/if}}
  </UkModal>
</template>
