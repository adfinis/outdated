import { concat, fn } from '@ember/helper';
import { on } from '@ember/modifier';
import { LinkTo } from '@ember/routing';
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import hasNext from 'ember-composable-helpers/helpers/has-next';
import slice from 'ember-composable-helpers/helpers/slice';
import formatDate from 'ember-intl/helpers/format-date';
import ukTooltip from 'ember-uikit/modifiers/uk-tooltip';

import EOLForm from './eol-form';

export const ProjectCell = <template>
  <LinkTo
    class='uk-link-text'
    @route='projects.detailed'
    @model={{@project.id}}
  >{{@project.name}}</LinkTo>
</template>;

export const DependencyCell = <template>
  <LinkTo
    class='uk-link-text'
    @route='dependencies.detailed'
    @model={{@dependency.id}}
  >{{@dependency.name}}</LinkTo>
</template>;

export const VersionCell = <template>
  <LinkTo
    class='uk-link-text'
    @route='versions.detailed'
    @model={{@version.id}}
  >{{@version.version}}</LinkTo>
</template>;

export const MaintainersCell = <template>
  {{#each @maintainers as |m|}}
    <span {{(modifier ukTooltip m.user.email pos='bottom')}}>
      {{concat
        m.user.username
        (if (hasNext m (slice @maintainers)) ',' '')
      }}</span>
  {{/each}}
</template>;

export class EndOfLifeCell extends Component {
  @tracked isEditing = false;

  setIsEditing = (value) => {
    this.isEditing = value;
  };

  <template>
    <EOLForm
      @version={{@version}}
      @setIsEditing={{this.setIsEditing}}
      @isEditing={{this.isEditing}}
    />
    {{#let @version.releaseVersion.endOfLife as |eol|}}
      <div
        class='{{if eol "" "uk-text-italic"}} uk-link-text cursor-pointer'
        tabindex='0'
        ...attributes
        {{on 'click' (fn (mut this.isEditing) true)}}
      >{{if eol (formatDate eol) 'undefined'}}</div>
    {{/let}}
  </template>
}
