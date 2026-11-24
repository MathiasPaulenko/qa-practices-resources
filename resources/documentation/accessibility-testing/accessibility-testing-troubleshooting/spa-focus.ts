// Angular route change focus management — SPA accessibility
import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({ selector: 'app-root', template: '' })
export class AppComponent {
  constructor(private router: Router) {
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd)
    ).subscribe(() => {
      const mainHeading = document.querySelector('h1');
      if (mainHeading) {
        mainHeading.setAttribute('tabindex', '-1');
        mainHeading.focus();
      }
    });
  }
}
