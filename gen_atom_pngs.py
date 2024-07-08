"""
Create a atomic shell .PNG image file for a list of atoms, one per image.


Before running this code:
- inputs/shell_electrons.txt should contain the electron numbers of atoms
- Create the directory outputs/, images will be stored there.

Dependencies:
- pip install python-docx

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# reference:
# https://byjus.com/question-answer/draw-the-atomic-structures-of-some-elements/

def main():
    max_shells = 7  #  e.g. 118. Oganesson: 2, 8, 18, 32, 32, 18, 8

    # Radiis
    max_shell_radius = 1.15
    min_shell_radius = 0.2
    min_electron_radius = 0.05
    max_electron_radius = 0.15
    min_nucleus_half_width =  0.2
    max_nucleus_half_width =  0.5

    # Width, Height for matplotlib
    max_x = 2.6
    max_y = 2.6
    center_xy = (max_x/2, max_y/2)

    nucleus_image = mpimg.imread('images/star.png')

    # Read shell electron file
    f = open("inputs/shell_electrons.txt", 'r')
    # f = open("inputs/tmp_shell_electrons.txt", 'r') # For debugging
    line = f.readline()
    while line != "":
        dot_index = line.index('.')
        colon_index = line.index(':')

        # Extract atomic number, atom name, and electron counts from text.
        atomic_number = int(line[:dot_index])
        name = line[dot_index+2:colon_index]
        shell_electron_counts = [int(x) for x in line[colon_index+2:].split(',')]
        num_shells = len(shell_electron_counts)
        assert atomic_number == sum(shell_electron_counts)  # Sanity check.

        print (f"{atomic_number} // {name} // {shell_electron_counts}")

        # Figure setup
        fig, ax = plt.subplots(figsize=(8,8))
        plt.tight_layout()  # Reduce whitespace.
        ax.axis("off")  # Don't show axis.
        ax.set_ylim([0, max_y])
        ax.set_xlim([0, max_x])

        # Calculate nucleus size and plot it.
        nucleus_half_width = (min_nucleus_half_width +
            ((max_nucleus_half_width-min_nucleus_half_width) *
             (float(max_shells-num_shells)/max_shells)))

        ax.imshow(nucleus_image,
            extent=[center_xy[0]-nucleus_half_width, center_xy[0]+nucleus_half_width,
                    center_xy[1]-nucleus_half_width, center_xy[1]+nucleus_half_width])

        # Iterate each shell of this atom and plot them with electrons
        for shell_index in range(num_shells):
            num_electrons = shell_electron_counts[shell_index]

            # Calculate shell radius, create circle, add to plot
            shell_radius = (min_shell_radius +
                ((shell_index+1) * (max_shell_radius-min_shell_radius)/num_shells))
            shell_circle = plt.Circle(
                center_xy, shell_radius, fill=False,
                linewidth=3, edgecolor='k')
            ax.add_patch(shell_circle)

            # Calculate elctron radius for this shell
            electron_radius = (min_electron_radius +
                ((max_electron_radius-min_electron_radius) *
                 (float(max_shells-num_shells)/max_shells)))

            # Plot each electron equally spaced along the perimeter of the shell
            for e in range(num_electrons):
                angle = e * (2*np.pi/num_electrons)
                x_offset = shell_radius * np.cos(angle)
                y_offset = shell_radius * np.sin(angle)

                point_xy = (center_xy[0]+x_offset, center_xy[1]+ y_offset)
                electron_circle = plt.Circle(point_xy, electron_radius,
                    color='k')

                ax.add_patch(electron_circle)

        # Next atom
        line = f.readline()
        fig.savefig(f"outputs/{atomic_number}.{name}.png")
    plt.show()

if __name__ == "__main__":
    main()
