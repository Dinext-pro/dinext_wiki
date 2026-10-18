describe('Wiki selected-release regression', () => {
  let fixture
  before(() => {
    const password = Cypress.env('adminPassword')
    expect(password, 'isolated site admin password').to.be.a('string').and.not.be.empty
    cy.loginUpgrade('Administrator', password)
    cy.callUpgrade('wiki.tests.dinext_upgrade.prepare').then((response) => {
      fixture = response.body.message
      cy.loginUpgrade(fixture.user, fixture.password)
    })
  })

  after(() => {
    cy.leaveUpgradeApp()
    cy.loginUpgrade('Administrator', Cypress.env('adminPassword'))
    cy.callUpgrade('wiki.tests.dinext_upgrade.cleanup')
  })

  it('loads the upgraded application with its synthetic fixture', () => {
    cy.visit('/wiki-app/spaces/' + encodeURIComponent(fixture.space))
    cy.contains(fixture.title).should('be.visible')
    cy.callUpgrade('frappe.client.set_value', {
      doctype: 'Wiki Document', name: fixture.document,
      fieldname: 'content', value: 'Verified upgraded Wiki content',
    })
    cy.visit('/' + fixture.route.split('/').map(encodeURIComponent).join('/'))
    cy.contains('Verified upgraded Wiki content').should('be.visible')
  })
})
