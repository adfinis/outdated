import Component from '@glimmer/component';

import { DependencyCell, EndOfLifeCell, VersionCell } from './cells';
import Table from './table';

import { orderByEOL, statusToClass } from 'outdated/utils';

export default class VersionTableComponent extends Component {
  get data() {
    return orderByEOL(this.args.versions).map((version) => ({
      component: <template>
        <tr class='{{statusToClass version.status}}'>{{yield}}</tr>
      </template>,
      values: {
        dependency: <template>
          <DependencyCell @dependency={{version.releaseVersion.dependency}} />
        </template>,
        version: <template><VersionCell @version={{version}} /></template>,
        endOfLife: <template><EndOfLifeCell @version={{version}} /></template>,
        releaseDate: version.releaseDate,
      },
    }));
  }

  <template>
    <Table @data={{this.data}} @fallback='Found no matching versions' as |t|>
      <t.head />
      <t.body />
    </Table>
  </template>
}
