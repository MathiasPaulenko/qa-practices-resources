/**
 * Minimal CMP consent-gate model for the cookie-consent test-cases article.
 * Vendors register per category; the gate decides which may fire based on
 * the stored consent state, the policy version, and GPC — the three
 * scopes the article's cases exercise. Deliberately dependency-free so it
 * runs under plain `node --test`.
 */

export const CATEGORIES = ['necessary', 'analytics', 'marketing'];

export class ConsentGate {
  /**
   * @param {object} opts
   * @param {string} opts.version consent policy version
   * @param {Array<{name:string, category:string}>} opts.vendors
   * @param {boolean} opts.gpc browser sends Global Privacy Control
   */
  constructor({ version = '1.0', vendors = [], gpc = false } = {}) {
    this.version = version;
    this.gpc = gpc;
    this.vendors = new Map();          // name -> {category, addedIn}
    for (const v of vendors) this.registerVendor(v.name, v.category);
    // null = no decision yet; Map = category -> boolean
    this.consent = null;
    this.consentVersion = null;
  }

  registerVendor(name, category) {
    if (!CATEGORIES.includes(category)) {
      throw new Error(`unknown category: ${category}`);
    }
    this.vendors.set(name, { category, addedIn: this.version });
  }

  _consented(category) {
    if (category === 'necessary') return true;
    if (this.consent === null) return this.gpc === true ? false : false;
    return this.consent.get(category) === true;
  }

  /** Vendor may fire only if consented AND its addedIn is covered by the consent version. */
  vendorAllowed(name) {
    const v = this.vendors.get(name);
    if (!v) return false;
    if (v.category === 'necessary') return true;
    if (!this._consented(v.category)) return false;
    // vendor added in a later version is not covered by earlier consent
    return v.addedIn <= (this.consentVersion ?? '0');
  }

  activeVendors() {
    return [...this.vendors.keys()].filter((n) => this.vendorAllowed(n));
  }

  hasConsent() {
    return this.consent !== null;
  }

  /** Banner shows when no decision exists or a re-prompt is required — unless GPC auto-rejects. */
  bannerVisible() {
    if (this.gpc && this.consent === null) return false; // auto-reject default
    return this.consent === null || this.needsReprompt();
  }

  /** Grant consent for the listed categories (necessary always implied). */
  grant(categories = CATEGORIES) {
    this.consent = new Map(CATEGORIES.map((c) => [c, categories.includes(c)]));
    this.consent.set('necessary', true);
    this.consentVersion = this.version;
  }

  /** Withdraw consent for a category — trackers must stop and cookies expire. */
  withdraw(category) {
    if (this.consent === null) return;
    this.consent.set(category, false);
  }

  /** Bump the policy version — prior consent no longer covers the new scope. */
  bumpVersion(newVersion) {
    this.version = newVersion;
  }

  needsReprompt() {
    if (this.consent === null) return false;
    return this.consentVersion !== this.version;
  }

  /** Serialize/restore the stored decision (session persistence). */
  serialize() {
    return this.consent === null
      ? null
      : JSON.stringify({ version: this.consentVersion, choices: [...this.consent] });
  }

  static restore(gate, blob) {
    if (blob === null) return;
    const { version, choices } = JSON.parse(blob);
    gate.consent = new Map(choices);
    gate.consentVersion = version;
  }
}
