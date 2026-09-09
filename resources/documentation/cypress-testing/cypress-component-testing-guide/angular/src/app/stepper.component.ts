import { Component, Input, Output, EventEmitter } from '@angular/core'

@Component({
  selector: 'app-stepper',
  template: `
    <button data-cy="increment" (click)="increment()">+</button>
    <span data-cy="counter">{{ count }}</span>
  `,
})
export class StepperComponent {
  @Input() count = 0
  @Output() change = new EventEmitter<number>()

  increment() {
    this.count++
    this.change.emit(this.count)
  }
}
