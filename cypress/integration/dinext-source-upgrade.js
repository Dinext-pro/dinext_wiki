describe('Wiki selected-release regression', () => {
  let fixture
  before(() => {
    const password = Cypress.env('adminPassword')
    expect(password, 'isolated site admin password').to.be.a('string').and.not.be.empty
    cy.loginUpgrade('Administrator', password)
    cy.callUpgrade('wiki.tests.dinext_upgrade.prepare').then((response) => {
      fixture = response.body.message
    })
  })

  after(() => {
    cy.leaveUpgradeApp()
    cy.loginUpgrade('Administrator', Cypress.env('adminPassword'))
    cy.callUpgrade('wiki.tests.dinext_upgrade.cleanup')
  })

  it('edits and reads the published document', () => {
    cy.loginUpgrade(fixture.user, fixture.password)
    cy.visit('/wiki-app/spaces/' + encodeURIComponent(fixture.space))
    cy.contains(fixture.title).should('be.visible')
    cy.callUpgrade('frappe.client.set_value', {
      doctype: 'Wiki Document', name: fixture.document,
      fieldname: 'content', value: 'Verified upgraded Wiki content',
    })
    cy.visit('/' + fixture.route.split('/').map(encodeURIComponent).join('/'))
    cy.contains('Verified upgraded Wiki content').should('be.visible')
  })

  it('keeps a restricted space inaccessible to an authenticated reader', () => {
    const url = '/api/method/wiki.api.wiki_space.get_space_bootstrap'
    const qs = { space_id: fixture.restricted }
    cy.loginUpgrade(fixture.user, fixture.password)
    cy.request({ url, qs }).its('body.message.doc.name').should('eq', fixture.restricted)
    cy.clearCookies()
    cy.loginUpgrade(fixture.reader, fixture.readerPassword)
    cy.request({ url, qs, failOnStatusCode: false }).its('status').should('eq', 403)
  })
})
