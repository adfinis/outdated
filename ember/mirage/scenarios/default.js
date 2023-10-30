export default function (server) {
  /*
    Seed your development database using your factories.
    This data will not be loaded in your tests.
  */
  // server.createList('post', 10);
  server.createList('project', 3, 'withVersions');
  server.createList('project', 1);
  server.createList('project', 2, 'withMaintainers', 'withVersions');
  server.createList('user', 2);
}
