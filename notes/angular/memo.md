To create a table that can store a variable number of contents in Angular, you can use the `*ngFor` directive to dynamically render rows based on an array of data. Here's an example:

### Steps:
1. Define a data array in your component to hold the table contents.
2. Use an HTML table in the template and bind the rows to the data array using `*ngFor`.

### Example:

#### `my-angular-app/src/app/feature/testPage.component.ts`
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-test-page',
  templateUrl: './testPage.component.html',
  styleUrls: ['./testPage.component.css']
})
export class TestPageComponent {
  // Example data array
  tableData = [
    { id: 1, name: 'John Doe', age: 28 },
    { id: 2, name: 'Jane Smith', age: 34 },
    { id: 3, name: 'Alice Johnson', age: 25 }
  ];

  // Method to add a new row
  addRow() {
    const newId = this.tableData.length + 1;
    this.tableData.push({ id: newId, name: `User ${newId}`, age: 30 });
  }
}
```

#### `my-angular-app/src/app/feature/testPage.component.html`
```html
<div class="container mt-4">
  <table class="table table-bordered">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Age</th>
      </tr>
    </thead>
    <tbody>
      <tr *ngFor="let row of tableData">
        <td>{{ row.id }}</td>
        <td>{{ row.name }}</td>
        <td>{{ row.age }}</td>
      </tr>
    </tbody>
  </table>

  <button class="btn btn-primary" (click)="addRow()">Add Row</button>
</div>
```

### Explanation:
1. The `tableData` array holds the dynamic content for the table.
2. The `*ngFor` directive iterates over the `tableData` array to render rows.
3. The `addRow` method adds a new row to the table dynamically when the button is clicked.

This approach allows you to store and display a variable number of contents in the table.