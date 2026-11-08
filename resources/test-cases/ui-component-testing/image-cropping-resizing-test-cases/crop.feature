Feature: Image cropping and resizing
  As a user editing an image
  I want to crop and resize it through the editor
  So that the exported file matches what I selected

  Background:
    Given the image editor is open
    And a 1200x800 JPEG is loaded

  Scenario: Basic crop preserves the selected region
    When I drag a crop area of 400x400 over the image
    And I apply the crop
    Then the exported image is 400x400
    And its pixels match the selected region

  Scenario: Locked aspect ratio cannot be broken by dragging
    Given the aspect ratio is locked to 1:1
    When I drag any corner handle to resize the crop area
    Then the selection stays square during the drag
    And the exported image is square

  Scenario: Portrait photo with EXIF orientation exports upright
    Given a portrait JPEG whose EXIF Orientation is 6
    When the editor renders the photo
    Then the preview shows the photo upright
    And a crop applied to it exports upright

  Scenario: Crop selection clamps at the image edge
    When I drag the crop area beyond the right edge of the image
    Then the selection stops at the image boundary
    And no coordinates outside the image are produced

  Scenario: Cancel discards the pending crop
    Given a crop area is selected but not applied
    When I press Cancel
    Then the original image is preserved
    And reopening the editor shows a clean state
