import { on } from '@ember/modifier';
import { get } from '@ember/object';
import EmberFlatpickr from 'ember-flatpickr/components/ember-flatpickr';
import { and, or } from 'ember-truth-helpers';

const onUpdate = (update, key) => (value) => {
  update(get(value, key));
};

const Text = <template>
  <input
    {{on 'input' (onUpdate @update 'target.value')}}
    {{on 'blur' @setDirty}}
    class='uk-input {{if @isValid "is-valid"}} {{if @isInvalid "is-invalid"}}'
    ...attributes
  />
</template>;

const Date = <template>
  <EmberFlatpickr
    placeholder={{@placeholder}}
    @dateFormat={{or @dateFormat 'Y-m-d'}}
    @date={{or @value null}}
    @onChange={{onUpdate @update 0}}
    @onClose={{@setDirty}}
    @allowInput={{or @allowInput true}}
    class='uk-input {{if @isValid "is-valid"}} {{if @isInvalid "is-invalid"}}'
  />
</template>;

const Select = <template>
  <@selectComponent
    @searchEnabled={{@searchable}}
    @options={{@options}}
    @selected={{@value}}
    @onChange={{@update}}
    @onClose={{@setDirty}}
    @searchField={{@searchField}}
    @placeholder={{@placeholder}}
    @renderInPlace={{true}}
    @afterOptionsComponent={{@afterOptionsComponent}}
    @optionsComponent={{@optionsComponent}}
    @searchMessage={{@searchMessage}}
    @noMatchesMessage={{@noMatchesMessage}}
    @noMatchesMessageComponent={{@noMatchesMessageComponent}}
    id={{@inputId}}
    class='{{if @isValid "is-valid "}} {{if @isInvalid "is-invalid"}}'
    as |name|
  >
    {{or
      (and
        (or @visibleField @searchField)
        (get name (or @visibleField @searchField))
      )
      name
    }}
  </@selectComponent>
</template>;

export { Text, Date, Select };
