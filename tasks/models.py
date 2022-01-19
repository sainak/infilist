from django.db import models
from django.utils.safestring import mark_safe

from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_children(self):
        return self.children.all().order_by("-created_date")

    def render_html(self):
        html = f"""
        <li id="{self.id}">
            {self.title}
            <a href="/complete_task/{self.id}/">&nbsp;&nbsp;&nbsp;&nbsp;Done</a>
            <a href="/delete_task/{self.id}/">&nbsp;&nbsp;&nbsp;&nbsp;Delete</a>
        </li>
        """
        if self.completed:
            html = f"<strike>{html}</strike>"
        html += f"""
        <ul>
            <li>
                <div class="input-group mb-3">
                    <form action="/add_task/" class="form-inline">
                        <input type="hidden" name="parent" value="{self.id}">
                        <input class="form-control" type="text" name="task">
                        <div class="input-group-append">
                            <button class="btn" style="background:#481620 ; color:whitesmoke" type="submit">Add to Infilist</button>
                        </div>
                    </form>
                </div>
            </li>
        </ul>
        """
        if self.get_children():
            html += "<ul>"
            for child in self.get_children():
                html += child.render_html()
            html += "</ul>"
        return mark_safe(html)
