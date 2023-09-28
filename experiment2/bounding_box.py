class BoundingBox:
    def __init__(self, top_left, bottom_right, num_points):
        # Initialize the bounding box corners and the number of points
        self.x_min, self.y_max = top_left
        self.x_max, self.y_min = bottom_right
        self.num_points = num_points

    @property
    def width(self):
        """Return the width of the bounding box."""
        return self.x_max - self.x_min
    
    @property
    def height(self):
        """Return the height of the bounding box."""
        return self.y_max - self.y_min

    @property
    def area(self):
        """Return the area of the bounding box."""
        return self.width * self.height

    @property
    def density(self):
        """Return the density of points in the bounding box."""
        return self.num_points / self.area

    @property
    def mean(self):
        """Estimate and return the mean coordinates of the points based on the bounding box."""
        mean_x = (self.x_min + self.x_max) / 2
        mean_y = (self.y_min + self.y_max) / 2
        return mean_x, mean_y

    @property
    def std_dev(self):
        """Estimate and return the standard deviation in x and y directions based on the bounding box."""
        std_dev_x = self.width / (12 ** 0.5)
        std_dev_y = self.height / (12 ** 0.5)
        return std_dev_x, std_dev_y

# Example usage remains the same
bbox = BoundingBox(top_left=(1, 5), bottom_right=(4, 1), num_points=100)
bbox_mean = bbox.mean
bbox_std_dev = bbox.std_dev

print(bbox_mean, bbox_std_dev)
