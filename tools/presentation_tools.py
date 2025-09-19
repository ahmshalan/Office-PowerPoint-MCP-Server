"""
Presentation management tools for PowerPoint MCP Server.
Handles presentation creation, opening, saving, and core properties.
"""
from typing import Dict, List, Optional, Any
import os
from fastmcp import FastMCP 
import utils as ppt_utils


def register_presentation_tools(app: FastMCP, presentations: Dict, get_current_presentation_id, get_template_search_directories):
    """Register presentation management tools with the FastMCP app"""
    
    @app.tool()
    def create_presentation(id: Optional[str] = None) -> Dict:
        """Create a new PowerPoint presentation."""
        # Create a new presentation
        pres = ppt_utils.create_presentation()
        
        # Generate an ID if not provided
        if id is None:
            id = f"presentation_{len(presentations) + 1}"
        
        # Store the presentation
        presentations[id] = pres
        # Set as current presentation (this would need to be handled by caller)
        
        return {
            "presentation_id": id,
            "message": f"Created new presentation with ID: {id}",
            "slide_count": len(pres.slides)
        }
        
    @app.tool()
    def open_presentation(file_path: str, id: Optional[str] = None) -> Dict:
        """Open an existing PowerPoint presentation from a file."""
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "error": f"File not found: {file_path}"
            }
        
        # Open the presentation
        try:
            pres = ppt_utils.open_presentation(file_path)
        except Exception as e:
            return {
                "error": f"Failed to open presentation: {str(e)}"
            }
        
        # Generate an ID if not provided
        if id is None:
            id = f"presentation_{len(presentations) + 1}"
        
        # Store the presentation
        presentations[id] = pres
        
        return {
            "presentation_id": id,
            "message": f"Opened presentation from {file_path} with ID: {id}",
            "slide_count": len(pres.slides)
        }

    @app.tool()
    def save_presentation(file_path: str, presentation_id: Optional[str] = None) -> Dict:
        """Save a presentation to a file."""
        # Use the specified presentation or the current one
        pres_id = presentation_id if presentation_id is not None else get_current_presentation_id()
        
        if pres_id is None or pres_id not in presentations:
            return {
                "error": "No presentation is currently loaded or the specified ID is invalid"
            }
        
        # Save the presentation
        try:
            saved_path = ppt_utils.save_presentation(presentations[pres_id], file_path)
            return {
                "message": f"Presentation saved to {saved_path}",
                "file_path": saved_path
            }
        except Exception as e:
            return {
                "error": f"Failed to save presentation: {str(e)}"
            }

    @app.tool()
    def get_presentation_info(presentation_id: Optional[str] = None) -> Dict:
        """Get information about a presentation."""
        pres_id = presentation_id if presentation_id is not None else get_current_presentation_id()
        
        if pres_id is None or pres_id not in presentations:
            return {
                "error": "No presentation is currently loaded or the specified ID is invalid"
            }
        
        pres = presentations[pres_id]
        
        try:
            info = ppt_utils.get_presentation_info(pres)
            info["presentation_id"] = pres_id
            return info
        except Exception as e:
            return {
                "error": f"Failed to get presentation info: {str(e)}"
            }


    @app.tool()
    def set_core_properties(
        title: Optional[str] = None,
        subject: Optional[str] = None,
        author: Optional[str] = None,
        keywords: Optional[str] = None,
        comments: Optional[str] = None,
        presentation_id: Optional[str] = None
    ) -> Dict:
        """Set core document properties."""
        pres_id = presentation_id if presentation_id is not None else get_current_presentation_id()
        
        if pres_id is None or pres_id not in presentations:
            return {
                "error": "No presentation is currently loaded or the specified ID is invalid"
            }
        
        pres = presentations[pres_id]
        
        try:
            ppt_utils.set_core_properties(
                pres,
                title=title,
                subject=subject,
                author=author,
                keywords=keywords,
                comments=comments
            )
            
            return {
                "message": "Core properties updated successfully"
            }
        except Exception as e:
            return {
                "error": f"Failed to set core properties: {str(e)}"
            }